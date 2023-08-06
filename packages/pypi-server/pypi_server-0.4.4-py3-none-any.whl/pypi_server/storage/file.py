# encoding: utf-8
import hashlib

import os
from collections import namedtuple
from .metadata import PackageMetadata
from ..cache import Cache, MINUTE


class File(file):
    __slots__ = ('__close_callbacks',)

    def __init__(self, name, mode='rb'):
        self.__close_callbacks = set()
        super(File, self).__init__(name, mode)

    def add_close_callback(self, cb):
        self.__close_callbacks.add(cb)

    def close(self):
        super(File, self).close()
        for cb in list(self.__close_callbacks):
            try:
                cb(self)
            except:
                pass


class PackageFile(namedtuple("PackageFileBase", "path name version")):
    CHUNK_SIZE = 2 ** 16

    def __init__(self, *args, **kwargs):
        super(PackageFile, self).__init__(*args, **kwargs)
        self.__metadata = self._metadata(self.path)

    def open(self, mode='rb'):
        f = File(self.path, mode)

        def metadata_update(f):
            with self.metadata as metadata:
                stat = os.stat(self.path)
                metadata['ts'] = stat.st_mtime
                metadata['size'] = stat.st_size

                md5 = hashlib.md5()
                with open(self.path, 'rb') as fl:
                    data = fl.read(self.CHUNK_SIZE)
                    md5.update(data)
                    while data:
                        data = fl.read(self.CHUNK_SIZE)
                        md5.update(data)

                    metadata['md5'] = md5.hexdigest()

        if any(x in mode for x in 'wa'):
            f.add_close_callback(metadata_update)

        return f

    def exists(self):
        return os.path.exists(self.path) and os.path.isfile(self.path)

    @property
    def metadata(self):
        return self.__metadata

    @classmethod
    @Cache(5 * MINUTE)
    def _metadata(cls, fname):
        meta = PackageMetadata("{0}.metadata".format(fname))
        meta.read()
        return meta
