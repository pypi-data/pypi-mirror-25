# encoding: utf-8
import os
from collections import namedtuple
from ..cache import Cache, MINUTE
from .file import PackageFile
from .pkg_dir import PackageDirectory


class PackageVersion(PackageDirectory, namedtuple("PackageVersionBase", "name path package")):
    @Cache(5 * MINUTE, ignore_self=True, oid="package_version_files")
    def files(self):
        return tuple(
            set(
                map(
                    lambda x: PackageFile(
                        version=self,
                        path=os.path.join(self.path, x),
                        name=os.path.basename(x)
                    ),
                    filter(
                        lambda x: os.path.isfile(x) and not x.endswith('.metadata'),
                        map(
                            lambda x: os.path.join(self.path, x),
                            os.listdir(self.path)
                        )
                    )
                )
            )
        )

    def find_file(self, name):
        for f in filter(lambda x: x.name == name, self.files()):
            return f
        raise LookupError("File not found")

    def create_file(self, name):
        name = os.path.basename(name)
        package_file = PackageFile(
            version=self,
            path=os.path.join(self.path, name),
            name=name,
        )

        Cache.invalidate("package_version_files")
        return package_file
