# -*- coding: utf-8 -*-
"""
Python module encapsulation.
"""
from __future__ import absolute_import, unicode_literals
from os.path import abspath, basename

import attr

from .. import rst
from .base import DocObjBase


@attr.s
class Module(DocObjBase):
    """
    Represents a python module. This is all the information needed to generate
    the documentation for the given module.
    """
    @classmethod
    def create(cls, path, owner=None):
        """
        Create a new module from the given path.

        :param str|unicode path:
            Path to the python module file.
        :param Package owner:
            The module owner. This is the package the module belongs to.
        :return Module:
            Newly created Module instance.
        """
        if not Module.is_module(path):
            raise ValueError("Not a module: {}".format(path))

        name = basename(path)[0:-3]
        mod = Module(
            path=abspath(path),
            name=name,
            fullname=name,
            owner=owner
        )

        if owner is not None:
            mod.fullname = owner.get_relative_name(mod)

        return mod

    @classmethod
    def is_module(cls, path):
        """ Return *True* if the given path is a python module. """
        return path.endswith('.py') and basename(path) != '__init__.py'

    @property
    def type(self):
        """ Hard override of the base .type property. """
        return 'module'

    def to_rst(self):
        """ Return reST document describing this module. """
        doc_src = rst.title('``{}``'.format(self.fullname))
        doc_src += rst.automodule(self.fullname)

        return doc_src

    def __str__(self):
        """ Return the package fullname as it's string representation. """
        return self.fullname
