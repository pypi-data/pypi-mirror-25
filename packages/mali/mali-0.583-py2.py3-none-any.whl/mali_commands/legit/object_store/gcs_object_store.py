# coding=utf-8
import logging
import random
import datetime
import requests
from threading import Semaphore

import httplib2
import time
import io
import os
from ..dulwich.object_store import BaseObjectStore
from ..dulwich.objects import hex_to_filename, hex_to_sha, sha_to_hex, ShaFile
from googleapiclient.discovery import build_from_document
from googleapiclient.http import MediaInMemoryUpload, MediaIoBaseDownload, HttpRequest
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from multiprocessing import Pool

from mali_commands.commons import url_encode

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GCSService(object):
    RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)
    CHUNKSIZE = 2 * 1024 * 1024
    DEFAULT_MIMETYPE = 'application/octet-stream'
    NUM_RETRIES = 5

    def __init__(self, signed_url_service):
        self.signed_url_service = signed_url_service
        self.__service = None

    def _get_authenticated_service(self):
        credentials = GoogleCredentials.get_application_default()

        if self.__service is None:
            discovery_file = os.path.join(os.path.dirname(__file__), 'gcs-v1.json')

            with open(discovery_file, encoding='utf8') as f:
                doc = f.read()
                self.__service = build_from_document(doc, http=credentials.authorize(httplib2.Http()))
        else:
            self.__service._http = credentials.authorize(httplib2.Http())

        return self.__service


def do_upload(bucket_name, object_name, body, signed_url_service=None):
    GCSUpload(signed_url_service).upload(bucket_name, object_name, body)


def do_download(bucket_name, object_name, signed_url_service=None):
    return GCSDownload(signed_url_service).download(bucket_name, object_name)


class GCSDownload(GCSService):
    def download(self, bucket_name, object_name):
        request = self._get_request(bucket_name, object_name)
        fd = io.BytesIO()
        media = MediaIoBaseDownload(fd, request, chunksize=self.CHUNKSIZE)

        retries = 0
        done = False
        while not done:
            error = None
            try:
                progress, done = media.next_chunk()
            except HttpError as err:
                if err.resp.status < 500:
                    raise
            except self.RETRYABLE_ERRORS as err:
                error = err

            if error:
                retries += 1

                if retries == self.NUM_RETRIES:
                    raise Exception()  # FIXME better Exception
            else:
                retries = 0

        data = fd.getvalue()
        logger.debug('downloaded  %s(%s)', object_name, len(data))

        return data

    def _get_request(self, bucket_name, object_name):
        if not self.signed_url_service:
            service = self._get_authenticated_service()
            return service.objects().get_media(bucket=bucket_name, object=object_name)

        url = self.signed_url_service.get_signed_urls('GET', [object_name])
        if not url:
            raise Exception()  # FIXME better Exception
        url = url[0]

        http = httplib2.Http()
        return HttpRequest(http, None, url)


class GCSUpload(GCSService):
    def upload(self, bucket_name, object_name, body):
        logger.debug('upload %s (%s)', object_name, '{:,}'.format(len(body)))
        start_time = datetime.datetime.utcnow()

        request = self._get_request(bucket_name, object_name, body)

        retries = 0
        response = None

        def progress_upload():
            return request.next_chunk()

        def simple_upload():
            current_response = request.execute()

            return current_response, 1

        upload_method = progress_upload if request.resumable else simple_upload
        while response is None:
            error = None
            try:
                progress, response = upload_method()
            except HttpError as err:
                error = err
                if err.resp.status < 500:
                    raise
            except self.RETRYABLE_ERRORS as err:
                error = err

            if error:
                retries += 1

                if retries == self.NUM_RETRIES:
                    raise Exception()  # FIXME better Exception

                sleep_time = random.random() * (2 ** retries)
                time.sleep(sleep_time)

        logger.debug('upload took %s', datetime.datetime.utcnow() - start_time)

    def _get_request(self, bucket_name, object_name, body):
        if not self.signed_url_service:
            service = self._get_authenticated_service()
            resumable = len(body) > self.CHUNKSIZE
            media = MediaInMemoryUpload(body, self.DEFAULT_MIMETYPE, chunksize=self.CHUNKSIZE, resumable=resumable)

            return service.objects().insert(bucket=bucket_name, name=object_name, media_body=media)

        # TODO: support resumable
        url = self.signed_url_service.get_signed_urls('PUT', [object_name])
        if not url:
            raise Exception()  # FIXME better Exception
        url = url[0]

        media = MediaInMemoryUpload(body, mimetype=self.DEFAULT_MIMETYPE, chunksize=self.CHUNKSIZE, resumable=False)
        http = httplib2.Http()

        def post_proc(resp, content):
            return resp, content

        return HttpRequest(http, post_proc, url, method='PUT', body=media.getbytes(0, media.size()))


class GCSObjectStore(BaseObjectStore):
    def __init__(self, volume_id, config, handle_api, bucket_name):
        self._signed_url_service = GCSSignedUrlService(volume_id, config, handle_api)
        # TODO: deprecate bucket_name
        self.__bucket_name = bucket_name
        self.__use_multiprocess = False
        self.__upload_pool = Pool(4)
        self.__max_waiting_semaphore = Semaphore(10)

    @classmethod
    def _get_shafile_path(cls, sha):
        # Check from object dir
        return hex_to_filename('objects', sha)

    def on_upload_result(self, result):
        self.__max_waiting_semaphore.release()

    @classmethod
    def on_upload_error(cls, ex):
        raise ex

    def add_object(self, obj):
        """Add a single object to this object store.

        :param obj: Object to add
        """

        path = self._get_shafile_path(obj.id)

        data = obj.as_legacy_object()

        if obj.type_name == b'blob':
            logger.debug(
                'uploading %s %s:%s %s bytes',
                path, obj.type_name, obj.type_num, '{:,}'.format(len(obj.data)))
        else:
            logger.debug(
                'uploading %s %s:%s\n%s (%s bytes)',
                path, obj.type_name, obj.type_num, obj.as_pretty_string(), '{:,}'.format(len(data)))

        if self.__use_multiprocess:
            self.__upload_pool.apply_async(
                do_upload, args=(self.__bucket_name, path, data), callback=self.on_upload_result,
                error_callback=self.on_upload_result)
            t = datetime.datetime.utcnow()
            self.__max_waiting_semaphore.acquire()
            print(datetime.datetime.utcnow() - t)
        else:
            do_upload(self.__bucket_name, path, data, signed_url_service=self._signed_url_service)

    def _get_loose_object(self, sha):
        logger.debug('get object %s', sha)
        path = self._get_shafile_path(sha)
        data = do_download(self.__bucket_name, path, signed_url_service=self._signed_url_service)
        return ShaFile.from_file(io.BytesIO(data))

    def get_raw(self, name):
        """Obtain the raw text for an object.

        :param name: sha for the object.
        :return: tuple with numeric type and object contents.
        """
        if len(name) == 40:
            sha = hex_to_sha(name)
            hex_sha = name
        elif len(name) == 20:
            sha = name
            hex_sha = None
        else:
            raise AssertionError("Invalid object name %r" % name)

        if hex_sha is None:
            hex_sha = sha_to_hex(name)

        ret = self._get_loose_object(hex_sha)
        if ret is not None:
            return ret.type_num, ret.as_raw_string()

        raise KeyError(hex_sha)


class GCSSignedUrlService(object):
    def __init__(self, volume_id, config, handle_api):
        self.volume_id = volume_id
        self.config = config
        self.handle_api = handle_api

    def get_signed_urls(self, method, object_names):
        params = {
            'method': method,
            'paths': object_names
        }
        url = 'data_volumes/{volume_id}/gcs_urls?{query_params}'.format(
            volume_id=self.volume_id, query_params=url_encode(params, True))

        result = self.handle_api(self.config, requests.get, url)

        return result['urls'] if result and 'urls' in result else None
