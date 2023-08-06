.. image:: https://circleci.com/gh/novopl/sphinx-refdoc.svg?style=shield&circle-token=6e5a5984421c7a4ec1de8efbe6e9ff10e6610e36
    :target: https://circleci.com/gh/novopl/sphinx-refdoc/tree/master

About
=====

**sphinx-refdoc** is a python reference documentation generator for Sphinx.


Installation
============

.. code-block:: shell

    $ pip install sphinx-refdoc


Usage
=====

.. code-block:: shell

    $ sphinx-refdoc <src_dir> <out_dir>

``sphinx-refdoc`` will parse you're source tree passed as the first parameter.
It will then generate a stub for sphinx reference documentation for that source.
It auto-generates all required files (one per module) and creates a navigation
based on the package structure of the source code.

It then saves it into the directory passed as the second argument. This will
usually be a subdirectory of the sphinx documentation directory. You can then
easily include the generated docs with you existing documentation by pointing
to the `<out_dir>/index.rst`.  Lets say you have a following directory
structure::

    docs/
    ├── ref/
    └── index.rst

where ``docs/ref`` is the directory containing the generated reference docs
(2nd argument of ``sphinx-refdoc`` invocation) and index.rst is the
documentation main index file (conf.py points to it). Then if you want to
include the reference documentation, you just need to add ``ref/index`` to the
toctree. For example:

.. code-block:: rst

    .. toctree::

        my_topic_1
        my_topic_2
        docs/ref


Contributing
============

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/sphinx-refdoc.git
    $ cd sphinx-refdoc
    $ virtualenv env
    $ source ./env/bin/activate
    $ ./devinit.sh


.. toctree::
    :maxdepth: 3

    docs/ref/index
