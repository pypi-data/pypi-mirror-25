# coding=utf-8
from .base_db_index import BaseMLIndex
from .cache import DatastoreTreeCache, GAEDatastoreTreeCache
from ..db import DatastoreConnection, GAEDatastoreConnection


class BigQueryMLIndex(BaseMLIndex):
    def __init__(self, connection):
        self.__table = None

        self.__create_tree_cache(connection)
        super(BigQueryMLIndex, self).__init__(connection)

    def __create_tree_cache(self, connection):
        if GAEDatastoreTreeCache is not None:
            datastore_connection = GAEDatastoreConnection(connection.data_volume_config)
        else:
            datastore_connection = DatastoreConnection(connection.data_volume_config, connection.project)

        tree_cache_class = GAEDatastoreTreeCache if GAEDatastoreTreeCache is not None else DatastoreTreeCache
        self.__tree_cache = tree_cache_class(datastore_connection)

    def __get_table(self, bq_dataset):
        if self.__table is not None:
            return self.__table

        table_full_name = '{prefix}_{name}'.format(prefix=self._connection.table_prefix, name='index')

        return bq_dataset.table(table_full_name)

    def _create_table_if_needed(self):
        from google.cloud import bigquery
        import google.api.core.exceptions

        with self._connection.get_cursor() as bq_dataset:
            table = self.__get_table(bq_dataset)

            table.schema = (
                bigquery.SchemaField('name', 'STRING', 'REQUIRED'),
                bigquery.SchemaField('sha', 'STRING', 'REQUIRED'),
                bigquery.SchemaField('ctime', 'INTEGER', 'REQUIRED'),
                bigquery.SchemaField('mtime', 'INTEGER', 'REQUIRED'),
                bigquery.SchemaField('mode', 'INTEGER', 'REQUIRED'),
                bigquery.SchemaField('uid', 'INTEGER', 'REQUIRED'),
                bigquery.SchemaField('gid', 'INTEGER', 'REQUIRED'),
                bigquery.SchemaField('size', 'INTEGER', 'REQUIRED'),
            )

            try:
                self.__table = table
                table.create()
            except google.api.core.exceptions.Conflict:
                pass

    def set_entries(self, entries):
        if not entries:
            return

        rows = self._decode_entries(entries)

        with self._connection.get_cursor() as bq_dataset:
            table = self.__get_table(bq_dataset)

            self.__tree_cache.set_entries(entries)

            table.insert_data(rows)

    def get_commit_id(self):
        return self.__tree_cache.get_commit_id()
