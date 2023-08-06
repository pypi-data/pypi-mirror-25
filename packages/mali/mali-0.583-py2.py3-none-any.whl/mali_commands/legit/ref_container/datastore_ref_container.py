# coding=utf-8
from ..dulwich.refs import RefsContainer


SYMREF = b'ref: '


class DatastoreRefContainer(RefsContainer):
    def __init__(self, connection):
        self.__connection = connection

    def __build_key(self, datastore, name):
        org_name = self.__connection.data_volume_config.org
        parent_key = datastore.key('DataVolume', self.__connection.data_volume_config.name, namespace=org_name)

        return datastore.key('DataVolumeRef', name, parent=parent_key, namespace=org_name)

    def get_packed_refs(self):
        return {}

    def set_if_equals(self, name, old_ref, new_ref):
        self._check_refname(name)

        name = name.decode('ascii')
        old_ref = old_ref.decode('ascii')
        new_ref = new_ref.decode('ascii')

        def txn(key):
            with datastore_client.transaction():
                ref_entity = datastore_client.get(key)

                if ref_entity is None:
                    return False

                if ref_entity['data'] != old_ref:
                    return False

                entity = self.__connection.create_entity(key)
                entity['data'] = new_ref
                datastore_client.put(entity)

                return True

        with self.__connection.get_cursor() as datastore_client:
            ref_key = self.__build_key(datastore_client, name)

            return txn(ref_key)

    def add_if_new(self, name, ref):
        self._check_refname(name)

        name = name.decode('ascii')
        ref = ref.decode('ascii')

        def txn(key):
            with datastore_client.transaction():
                ref_entity = datastore_client.get(key)

                if ref_entity is not None:
                    return False

                entity = self.__connection.create_entity(key)
                entity['data'] = ref
                datastore_client.put(entity)

                return True

        with self.__connection.get_cursor() as datastore_client:
            ref_key = self.__build_key(datastore_client, name)

            return txn(ref_key)

    def read_loose_ref(self, name):
        """Read a reference and return its contents.

        If the reference file a symbolic reference, only read the first line of
        the file. Otherwise, only read the first 40 bytes.

        :param name: the refname to read, relative to refpath
        :return: The contents of the ref file, or None if the file does not
            exist.
        """

        with self.__connection.get_cursor() as datastore:
            ref_key = self.__build_key(datastore, name.decode('utf8'))
            ref = datastore.get(ref_key)

            if ref is None:
                return None

            data = ref['data']

            header = data[:len(SYMREF)]
            if header == SYMREF:
                # Read only the first line
                return data.splitlines()[0]

            # Read only the first 40 bytes
            return data[:40].encode('ascii')
