# -*- coding: utf-8 -*-
"""
Sphinx toctree directive generator.
"""
from __future__ import absolute_import
from os.path import splitext

import attr


@attr.s
class Toctree(object):
    """ This class helps building Sphinx toctrees.

    :param int maxdepth:
        The number of levels included in the TOC. If the TOC entry has
        children and ``maxdepth > 1`` those children will be inlined
        as well. This makes the toctree a tree.
    """
    maxdepth = attr.ib(default=1)
    entries = attr.ib(default=None)
    hidden = attr.ib(default=False)

    def add(self, entry):
        """ Add entry to the TOC.

        :param str|unicode entry:
            This is a relative path to the ReST file. The function can
            correctly handle cases where the path is given with the ext or
            without (as Sphinx uses file names without the extension for
            toctree entries).
        """
        if self.entries is None:
            self.entries = []

        name, _ = splitext(entry)
        self.entries.append(name)

    def __str__(self):
        """
        :return str:
            The sphinx ``toctree`` directive.
        """
        rst_src = [
            '.. toctree::',
            '    :maxdepth: {}'.format(self.maxdepth),
        ]
        if self.hidden:
            rst_src.append('    :hidden:')

        if self.entries:
            rst_src.append('')
            rst_src += ['    ' + e for e in self.entries]

        rst_src.append('')

        return '\n'.join(rst_src)
