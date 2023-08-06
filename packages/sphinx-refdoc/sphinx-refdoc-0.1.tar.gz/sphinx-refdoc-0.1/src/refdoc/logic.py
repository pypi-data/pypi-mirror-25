# -*- coding: utf-8 -*-
"""
The actual documentation generation happens here.
"""
from __future__ import absolute_import, unicode_literals
import os
from os.path import exists, join

from . import rst
from .objects import Package
from .toctree import Toctree


def generate_docs(pkg_paths, out_dir):
    """ Generate documentation for the given package list. """
    pkgs = [Package.create(p) for p in pkg_paths]

    with open(join(out_dir, 'index.rst'), 'w') as fp:
        fp.write(generate_root_index_rst(pkgs))

    for pkg in pkgs:
        generate_pkg_docs(pkg, out_dir)


def generate_root_index_rst(packages):
    """ Generate root package index file. """
    toc = Toctree()
    for pkg in packages:
        toc.add(join(pkg.name + '/index.rst'))

    src = rst.title('Reference documentation')
    src += str(toc)

    return src


def generate_pkg_docs(pkg, out_dir):
    """ Generate documentation for the given package in the given out_dir. """
    pkg.collect_children()
    pkg_path = join(out_dir, pkg.name)

    if not exists(pkg_path):
        os.makedirs(pkg_path)

    # Generate the package documentation
    with open(join(pkg_path, 'index.rst'), 'w') as fp:
        fp.write(pkg.to_rst())

    # Generate documentation for all the children
    for child in pkg.children:
        if child.type == 'package':
            generate_pkg_docs(child, pkg_path)
        elif child.type == 'module':
            generate_module_docs(child, pkg_path)
        else:
            print("Unknown child type '{}'".format(child.type))


def generate_module_docs(module, out_dir):
    """ Generate documentation for the given module in the given out_dir. """
    with open(join(out_dir, module.name + '.rst'), 'w') as fp:
        fp.write(module.to_rst())
