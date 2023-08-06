# -*- coding: utf-8 -*-
"""
Python package encapsulation
"""
from __future__ import absolute_import, unicode_literals
import os
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import join
from os.path import sep as path_sep

import attr

from .. import rst
from ..toctree import Toctree
from .module import Module
from .base import DocObjBase


@attr.s
class Package(DocObjBase):
    """
    Represents a python package. This is all the information needed to generate
    the documentation for the given package.
    """
    children = attr.ib(default=[])

    @classmethod
    def create(cls, path, owner=None):
        """
        Create a new package from the given path.

        :param str|unicode path:
            Path to the python package directory.
        :param Package owner:
            The package owner. This is the package this package belongs to.
        :return Module:
            Newly created Package instance.
        """
        if not Package.is_pkg(path):
            raise ValueError('{} is not a package'.format(path))

        if owner is None:
            # Try detecting enclosing package
            if Package.is_pkg(join(path, '..')):
                owner = Package.create(join(path, '..'))

        name = basename(path)
        pkg = Package(
            path=abspath(path),
            name=name,
            fullname=name,
            owner=owner,
        )

        if owner is not None:
            pkg.fullname = owner.get_relative_name(pkg)

        return pkg

    @classmethod
    def is_pkg(cls, path):
        """ Return ``True`` if the given path is a python package. """
        return exists(join(path, '__init__.py'))

    @property
    def type(self):
        """ Hard override of the base .type property. """
        return 'package'

    def __str__(self):
        """ Return the package fullname as it's string representation. """
        return self.fullname

    def get_relative_name(self, obj):
        """ Get the obj full python name relative to this package.

        :param Package|Module obj:
            The object you want the path for.
        :return unicode:
            The full python path for the given object. This is the same
            notation as used in python import statements
        """
        basedir = dirname(self.path)
        curr_dir = dirname(obj.path)

        parents = []
        while Package.is_pkg(join(basedir, curr_dir)):
            parents.append(basename(curr_dir))

            if path_sep not in curr_dir:
                # We reached the basedir
                break

            curr_dir = dirname(curr_dir)

        return '.'.join(reversed(parents)) + '.' + obj.name

    def get_child(self, name):
        """ Get child module or package by name.

        :param str|unicode name:
            The name of the package/module you're looking for.
        :return Package|Module:
            The child package/module with the given name or *None* if not found.
        """
        return next((x for x in self.children if x.name == name), None)

    def collect_children(self, recursive=True):
        """ Collect all children of the package.

        This includes all modules and packages belonging to the current package.

        :param bool recursive:
            If *True* it will recursively collect all sub packages that belong
            to this package.
        """
        self.children = []

        for fname in os.listdir(self.path):
            path = join(self.path, fname)

            if Package.is_pkg(path):
                child = Package.create(path, owner=self)
                if recursive:
                    child.collect_children()

            elif Module.is_module(path):
                child = Module.create(path, owner=self)

            else:
                print("Unknown file type: {}".format(path))
                continue

            self.children.append(child)

    def to_rst(self):
        """ Return reST markdown to use for this package documentation. """
        rst_src = rst.title('``{}``'.format(self.fullname))
        rst_src += rst.autosummary([
            '{}'.format(m.fullname) for m in self.children
        ])
        rst_src += rst.automodule(self.fullname, members=False)

        toc = Toctree(hidden=True)
        for child in self.children:
            if child.type == 'package':
                toc.add(child.name + '/index')
            elif child.type == 'module':
                toc.add(child.name)

        rst_src += str(toc)

        return rst_src
