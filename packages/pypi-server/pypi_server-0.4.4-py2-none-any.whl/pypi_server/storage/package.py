# encoding: utf-8
import os
from collections import namedtuple
from . import AlreadyExists, HashVersion
from .version import PackageVersion
from .pkg_dir import PackageDirectory
from ..cache import Cache, HOUR


class Package(PackageDirectory, namedtuple("PackageBase", "name path")):
    @Cache(HOUR, oid='package_versions')
    def versions(self):
        return tuple(
            sorted(
                set(
                    map(
                        lambda x: PackageVersion(
                            package=self,
                            path=os.path.join(self.path, x),
                            name=HashVersion(os.path.basename(x))
                        ),
                        filter(
                            os.path.isdir,
                            map(
                                lambda x: os.path.join(self.path, x),
                                os.listdir(self.path)
                            )
                        )
                    )
                ),
                key=lambda x: x.name,
                reverse=True
            )
        )

    def find_version(self, name):
        for version in filter(lambda x: x.name == name, self.versions()):
            return version

        raise LookupError("Version not found")

    def create_version(self, name):
        name = os.path.basename(name)
        version = PackageVersion(
            package=self,
            name=HashVersion(os.path.basename(name)),
            path=os.path.join(self.path, name)
        )

        if version in self.versions():
            raise AlreadyExists("Version already exists")

        version.create()

        Cache.invalidate('package_versions')
        return version

    def get_or_create(self, name):
        try:
            return self.create_version(name)
        except AlreadyExists:
            return self.find_version(name)
