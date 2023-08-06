#!/usr/bin/env python
# encoding: utf-8
import os


class PackageDirectory(object):
    PATH_ATTR = 'path'

    def create(self):
        path = getattr(self, self.PATH_ATTR)
        if self.exists():
            return False

        os.makedirs(path)
        return True

    def exists(self):
        path = getattr(self, self.PATH_ATTR)
        return os.path.exists(path) and os.path.isdir(path)
