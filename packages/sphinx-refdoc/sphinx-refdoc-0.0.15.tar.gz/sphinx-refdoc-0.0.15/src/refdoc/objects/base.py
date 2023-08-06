# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os.path import basename, dirname, join, relpath, sep as path_sep

import attr


@attr.s
class PyObjectBase(object):
    """

    :var path:      Path to the package.
    :var name:      Package name.
    :var fullname:  Package fully qualified name.
    :var owner:     The enclosing package or *None* of none exists.
    """
    path = attr.ib()
    name = attr.ib()
    fullname = attr.ib()
    owner = attr.ib(default=None)

    @property
    def type(self):
        raise NotImplementedError("{} should implement .type()".format(
            self.__class__.__name__
        ))

    def to_rst(self):
        raise NotImplementedError("Models must implement .to_rst()")

    @property
    def base_path(self):
        if self.owner:
            return self.owner.base_path
        else:
            curr_dir = self.path

            parents = []
            while self.is_pkg(curr_dir):
                parents.append(basename(curr_dir))

                if path_sep not in curr_dir:
                    # We reached the rootdir
                    break

                curr_dir = dirname(curr_dir)

            return curr_dir

    @property
    def rel_path(self):
        return relpath(self.path, self.base_path)
