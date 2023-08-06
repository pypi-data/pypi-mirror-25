# -*- coding: utf-8 -*-
"""
Simple generators for reStructuredText directives.
"""
from __future__ import absolute_import
import itertools


def title(title):
    """ Generate reST title directive.

    :Examples:

    >>> section('Page title')
    '''
    ==========
    Page title
    ==========
    <BLANKLINE>
    '''

    """
    title_len  = len(title)
    return '\n'.join((
        '',
        '=' * title_len,
        title,
        '=' * title_len,
        '',
    ))


def section(name, underline_char='='):
    """ Generate reST section directive with the given underline.

    :Examples:

    >>> section('My section')
    '''
    My section
    ==========
    <BLANKLINE>
    '''

    >>> section('Subsection', '~')
    '''
    Subsection
    ~~~~~~~~~~
    <BLANKLINE>
    '''

    """
    name_len  = len(name)
    return '\n'.join((
        '',
        name,
        underline_char * name_len,
        '',
    ))


def automodule(name, members=True):
    """ Generate reST automodule directive for the given module.

    :Examples:

    >>> automodule('my.test.module')
    '''
    .. automodule:: my.test.module
        :members:
    <BLANKLINE>
    '''

    """
    lines = [
        '',
        '.. automodule:: {}'.format(name),
    ]
    if members:
        lines.append('    :members:')

    lines.append('')
    return '\n'.join(lines)


def autosummary(names):
    """ Generate reST automodule directive for the given module.

    :Examples:

    >>> autosummary(['my.test.module', 'my.test.module2'])
    '''
    .. autosummary::

        my.test.module1
        my.test.module2

    <BLANKLINE>
    '''

    """
    lines = itertools.chain(
        [
            '',
            '.. autosummary::',
            ''
        ],
        ['    {}'.format(name) for name in names],
        ['']
    )
    return '\n'.join(lines)
