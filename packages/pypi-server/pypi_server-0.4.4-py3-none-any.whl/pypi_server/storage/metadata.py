# encoding: utf-8
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle


class PackageMetadata(dict):
    __getattr__ = dict.__getitem__

    def __init__(self, path, **kwargs):
        super(PackageMetadata, self).__init__(**kwargs)
        self.__path = path

    def read(self):
        self.update(self._load(self.__path))

    def write(self):
        self._dump(self.__path, self)

    @classmethod
    def _load(cls, path):
        if not all(f(path) for f in (os.path.exists, os.path.isfile)):
            return ()

        with open(path, 'rb') as fd:
            return dict(pickle.load(fd))

    @classmethod
    def _dump(cls, path, data):
        with open(path, 'wb+') as fd:
            return pickle.dump(tuple(data.items()), fd, protocol=2)

    def __enter__(self):
        self.read()
        return self

    def __exit__(self, exc_type, *args):
        if exc_type:
            return

        self.write()
