# coding=utf-8
import os

from mali_commands.legit.dulwich.repo import Repo
from mali_commands.commons import handle_api
from mali_commands.data_volume_config import DataVolumeConfig
from mali_commands.legit.db import MySqlConnection, SqliteConnection, SpannerConnection, BigQueryConnection, \
    DatastoreConnection, BackendConnection
from mali_commands.legit.metadata_db.backend_metadata import BackendMetadataDB
from mali_commands.legit.object_store import GCSObjectStore, NullObjectStore
from mali_commands.legit.db_index import SqliteMLIndex, MySqlMLIndex, SpannerMLIndex, BigQueryMLIndex, BackendMLIndex
from mali_commands.legit.metadata_db import SqliteMetadataDB, MySqlMetadataDB, SpannerMetadataDB, BigQueryMetadataDB
from mali_commands.legit.ref_container import MySqlRefsContainer, SpannerRefContainer, DatastoreRefContainer


class MLIgnoreFilterManager(object):
    def is_ignored(self, relpath):
        return False


class MlRepo(Repo):
    def __init__(self, config, repo_root, read_only=False):
        self.__dv_config = DataVolumeConfig(repo_root)

        self.__in_transactions = False
        self.__config = config
        self.__connections = {}
        self.__read_only = read_only
        self.__metadata = None

        super(MlRepo, self).__init__(repo_root, self.data_volume_config.data_path)

    @property
    def _config(self):
        return self.__config

    def close(self):
        for connection in self.__connections.values():
            connection.close()

        super(MlRepo, self).close()

    def __create_connection(self, name, **kwargs):
        kwargs.update(self.data_volume_config.db_config)
        kwargs['read_only'] = self.__read_only
        kwargs['data_volume_config'] = self.data_volume_config

        if self.data_volume_config.db_type == 'sqlite':
            return SqliteConnection(**kwargs)

        if self.data_volume_config.db_type == 'mysql':
            return MySqlConnection(**kwargs)

        if self.data_volume_config.db_type == 'spanner':
            return SpannerConnection(**kwargs)

        if self.data_volume_config.db_type == 'bq' and name == 'datastore':
            return DatastoreConnection(**kwargs)

        if self.data_volume_config.db_type == 'bq':
            return BigQueryConnection(**kwargs)

        return BackendConnection(**kwargs)

    def start_transactions(self):
        for connection in self.__connections.values():
            connection.start_transactions()

        self.__in_transactions = True

    def end_transactions(self):
        for connection in self.__connections.values():
            connection.end_transactions()

        self.__in_transactions = False

    def _connection_by_name(self, name, **kwargs):
        if name not in self.__connections:
            connection = self.__create_connection(name, **kwargs)

            if self.__in_transactions:
                connection.start_transactions()

            self.__connections[name] = connection

        return self.__connections[name]

    @property
    def metadata(self):
        if self.__metadata is None:
            if self.data_volume_config.db_type == 'sqlite':
                metadata_path = os.path.join(self.repo_root, 'metadata.db')
                metadata = SqliteMetadataDB(self._connection_by_name('metadata', path=metadata_path))
            elif self.data_volume_config.db_type == 'mysql':
                metadata = MySqlMetadataDB(self._connection_by_name('main'))
            elif self.data_volume_config.db_type == 'spanner':
                metadata = SpannerMetadataDB(self._connection_by_name('main'))
            elif self.data_volume_config.db_type == 'bq':
                metadata = BigQueryMetadataDB(self._connection_by_name('metadata'))
            else:
                metadata = BackendMetadataDB(self._connection_by_name('metadata'), self._config, handle_api)

            self.__metadata = metadata

        return self.__metadata

    @property
    def data_volume_config(self):
        return self.__dv_config

    def open_index(self):
        if self.data_volume_config.db_type == 'sqlite':
            index_file_name = self.index_path()

            pre, ext = os.path.splitext(index_file_name)

            index_file_name = pre + '.db'

            return SqliteMLIndex(self._connection_by_name('index', path=index_file_name))

        if self.data_volume_config.db_type == 'mysql':
            return MySqlMLIndex(self._connection_by_name('main'))

        if self.data_volume_config.db_type == 'spanner':
            return SpannerMLIndex(self._connection_by_name('main'))

        if self.data_volume_config.db_type == 'bq':
            return BigQueryMLIndex(self._connection_by_name('main'))

        return BackendMLIndex(self._connection_by_name('main'), self._config, handle_api)

    def create_ref_container(self):
        if self.data_volume_config.object_store_type == 'disk':
            return super(MlRepo, self).create_ref_container()

        if self.data_volume_config.db_type == 'mysql':
            MySqlRefsContainer(self._connection_by_name('main'))

        if self.data_volume_config.db_type == 'spanner':
            return SpannerRefContainer(self._connection_by_name('main'))

        if self.data_volume_config.db_type == 'bq':
            return DatastoreRefContainer(self._connection_by_name('datastore'))

        raise NotImplemented()

    def create_object_store(self):
        if self.data_volume_config.object_store_type == 'disk':
            return super(MlRepo, self).create_object_store()

        if self.data_volume_config.object_store_type == 'null':
            return NullObjectStore()

        if self.data_volume_config.object_store_type == 'gcs':
            return GCSObjectStore(**self.data_volume_config.object_store_config)

        raise NotImplemented()

    def get_config_stack(self):
        return DataVolumeConfig(self.repo_root)

    def get_ignore_filter_manager(self):
        return MLIgnoreFilterManager()

    def _get_user_identity(self):
        import jwt

        data = jwt.decode(self._config.id_token, verify=False) if self.__config.id_token else {}

        return '{name} <{email}>'.format(**data).encode('utf8')
