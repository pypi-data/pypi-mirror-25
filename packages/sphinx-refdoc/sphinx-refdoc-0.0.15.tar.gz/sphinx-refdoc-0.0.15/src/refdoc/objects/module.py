# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from os.path import abspath, basename, relpath

import attr

from .. import rst
from .base import PyObjectBase


@attr.s
class Module(PyObjectBase):
    """
    Represents a python module. This is all the information needed to generate
    the documentation for the given module.
    """
    @classmethod
    def create(cls, path, owner=None):
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
        return path.endswith('.py') and basename(path) != '__init__.py'

    @property
    def type(self):
        return 'module'

    def to_rst(self):
        doc_src = rst.title('``{}``'.format(self.fullname))
        doc_src += rst.automodule(self.fullname)

        return doc_src

    def __str__(self):
        return self.fullname
