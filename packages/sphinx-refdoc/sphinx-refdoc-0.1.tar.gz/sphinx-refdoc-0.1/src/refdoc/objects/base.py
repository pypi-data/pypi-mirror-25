# -*- coding: utf-8 -*-
""" Base class for both Module and Package.

Contains shared functionality.
"""
from __future__ import absolute_import, unicode_literals

from os.path import basename, dirname, relpath, sep as path_sep

import attr


@attr.s
class DocObjBase(object):
    """ Base python object.

    This contains the shared code between Modules and Packages.

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
        """ The type of the object.

        Each derived class has to implement this property.
        """
        raise NotImplementedError("{} must implement .type()".format(
            self.__class__.__name__
        ))

    def to_rst(self):
        """ Convert the objec to reStructuredText.

        Each derived class has to implement this method.
        """
        raise NotImplementedError("Models must implement .to_rst()")

    @property
    def base_path(self):
        """ Return the module/package base path.

        This is the base used for generating module/package names.
        """
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
        """ The path relative to the base_path. """
        return relpath(self.path, self.base_path)
