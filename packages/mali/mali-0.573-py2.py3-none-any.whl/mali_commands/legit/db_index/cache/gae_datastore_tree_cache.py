# coding=utf-8
from ...connection_mixin import ConnectionMixin
from .tree_cache import TreeCache
from google.appengine.ext import ndb


class TreeCacheModel(ndb.Model):
    files = ndb.TextProperty(required=True)
    sha = ndb.StringProperty(required=True)

    @classmethod
    def _get_kind(cls):
        return 'TreeCache'


class GAEDatastoreTreeCache(ConnectionMixin, TreeCache):
    def __init__(self, connection):
        super(GAEDatastoreTreeCache, self).__init__(connection)

    def __build_key(self, name):
        org_name = self._connection.data_volume_config.org
        parent_key = ndb.Key('DataVolume', self._connection.data_volume_config.volume_id, namespace=org_name)

        name = name or 1

        return ndb.Key('TreeCache', name, parent=parent_key, namespace=org_name)

    def _set_files(self, trees_objects):
        inserts = []
        for path, tree in trees_objects.items():
            blob = '\n'.join(self.build_blob(tree))

            name = path.decode('utf8')

            entity = TreeCacheModel(key=self.__build_key(name), files=blob.encode('utf8'), sha=tree.id.decode('utf8'))

            inserts.append(entity)

        ndb.put_multi(inserts)

    def get_commit_id(self):
        entity = self.__build_key('').get()

        if entity is None:
            return None

        return entity.sha

    def _get_files(self, scans):
        def name_from_key(entity):
            entity_id = entity.key.id()
            return '' if entity_id == 1 else entity_id

        keys = [self.__build_key(path) for path, _, _ in scans]

        cache_entities = ndb.get_multi(keys)

        return {name_from_key(entity): self._files_sha_array_to_dict(entity.files) for entity in cache_entities if entity is not None}
