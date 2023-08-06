# encoding: utf-8
import os
from distutils.version import LooseVersion

from . import AlreadyExists
from .package import Package
from ..cache import Cache, HOUR


class Storage(object):
    CHUNK_SIZE = 2 ** 16

    def __init__(self, basedir):
        self.path = os.path.abspath(basedir)

    @Cache(HOUR, oid='package_list')
    def packages(self):
        return tuple(
            set(
                map(
                    lambda x: Package(
                        path=os.path.join(self.path, x),
                        name=os.path.basename(x)
                    ),
                    filter(
                        os.path.isdir,
                        map(
                            lambda x: os.path.join(self.path, x),
                            os.listdir(self.path)
                        )
                    )
                )
            )
        )

    def find_package(self, name):
        for package in self.packages():
            if package.name == name:
                return package

    def create_package(self, name):
        name = os.path.basename(name)
        pkg = Package(path=os.path.join(self.path, name), name=name)

        if pkg in self.packages():
            raise AlreadyExists("Package already exists")

        pkg.create()
        Cache.invalidate('package_list')
        return pkg
