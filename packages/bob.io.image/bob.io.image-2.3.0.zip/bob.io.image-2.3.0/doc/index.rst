.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Wed 14 May 15:22:33 2014 CEST
..
.. Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland

.. _bob.io.image:

===============================================
 Bob's I/O Routines for Images of Various type
===============================================

.. todolist::

This package is a part of `Bob`_.
It provides a plugin for :py:mod:`bob.io.base` that allows |project|
to read and write images using its native API (:py:func:`bob.io.base.load` and
:py:func:`bob.io.base.save`).

At present, this plugin provides support for the following types of images:

* TIFF (gray and color)
* JPEG (gray and color)
* GIF (color only)
* PNG (gray and color)
* BMP (color only)
* Netpbm images (binary - PBM, gray - PGM, color - PPM)

Additionally, we provide the pure C++ interface to read and write these kind of
images, see :doc:`cpp_api`.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api
   cpp_api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
