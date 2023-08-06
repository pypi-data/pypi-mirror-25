# coding=utf-8
import logging
import random
import datetime
from threading import Semaphore

import httplib2
import time
import io
import os
from ..dulwich.object_store import BaseObjectStore
from ..dulwich.objects import hex_to_filename, hex_to_sha, sha_to_hex, ShaFile
from googleapiclient.discovery import build_from_document
from googleapiclient.http import MediaInMemoryUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from multiprocessing import Pool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# logger.addHandler(logging.StreamHandler())


class GCSService:
    RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)
    CHUNKSIZE = 2 * 1024 * 1024
    DEFAULT_MIMETYPE = 'application/octet-stream'
    NUM_RETRIES = 5

    def __init__(self):
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


def do_upload(bucket_name, object_name, body):
    GCSUpload(bucket_name, object_name, body).upload()


def do_download(bucket_name, object_name):
    return GCSDownload(bucket_name, object_name).download()


class GCSDownload(GCSService):
    def __init__(self, bucket_name, object_name):
        super(GCSDownload, self).__init__()
        self.__bucket_name = bucket_name
        self.__object_name = object_name

    def download(self):
        service = self._get_authenticated_service()

        request = service.objects().get_media(bucket=self.__bucket_name, object=self.__object_name)
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
        logger.debug('downloaded  %s(%s)', self.__object_name, len(data))

        return data


class GCSUpload(GCSService):
    def __init__(self, bucket_name, object_name, body):
        super(GCSUpload, self).__init__()
        self.__bucket_name = bucket_name
        self.__object_name = object_name
        self.__body = body

    def upload(self):
        logger.debug('upload %s (%s)', self.__object_name, '{:,}'.format(len(self.__body)))

        service = self._get_authenticated_service()

        resumable = len(self.__body) > self.CHUNKSIZE

        media = MediaInMemoryUpload(self.__body, self.DEFAULT_MIMETYPE, chunksize=self.CHUNKSIZE, resumable=resumable)

        start_time = datetime.datetime.utcnow()

        request = service.objects().insert(bucket=self.__bucket_name, name=self.__object_name, media_body=media)

        retries = 0
        response = None

        def progress_upload():
            return request.next_chunk()

        def simple_upload():
            current_response = request.execute()

            return current_response, 1

        upload_method = progress_upload if resumable else simple_upload
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


class GCSObjectStore(BaseObjectStore):
    def __init__(self, bucket_name, **kwargs):
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
            do_upload(self.__bucket_name, path, data)

    def _get_loose_object(self, sha):
        logger.debug('get object %s', sha)
        path = self._get_shafile_path(sha)
        data = do_download(self.__bucket_name, path)
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
