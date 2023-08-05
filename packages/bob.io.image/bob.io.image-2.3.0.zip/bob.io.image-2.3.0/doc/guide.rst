.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.dos.anjos@gmail.com>
.. Fri 16 May 11:48:13 2014 CEST

.. testsetup:: *

   import numpy
   import bob.io.base
   import bob.io.image
   import tempfile
   import os

   current_directory = os.path.realpath(os.curdir)
   temp_dir = tempfile.mkdtemp(prefix='bob_doctest_')
   os.chdir(temp_dir)

   from bob.io.base import test_utils
   path_to_image = test_utils.datafile('grace_hopper.png', 'bob.io.image')

============
 User Guide
============

By importing this package, you can use |project| native array reading and
writing routines to load and save files using various image formats, using the
simple plug-in technology for :py:mod:`bob.io.base`, i.e.,
:py:func:`bob.io.base.load` and :py:func:`bob.io.base.save`.

.. doctest::

   >>> import bob.io.base
   >>> import bob.io.image  # under the hood: loads Bob plugin for image files
   >>> img = bob.io.base.load(path_to_image)

In the following example, an image generated randomly using the method `NumPy`
:py:func:`numpy.random.random_integers`, is saved in lossless PNG format. The
image must be of type ``uint8`` or ``uint16``:

.. doctest::

  >>> my_image = numpy.random.random_integers(0,255,(3,256,256))
  >>> bob.io.base.save(my_image.astype('uint8'), 'testimage.png') # saving the image in png format
  >>> my_image_copy = bob.io.base.load('testimage.png')
  >>> assert (my_image_copy == my_image).all()

The loaded image files can be 3D arrays (for RGB format) or 2D arrays (for
greyscale) of type ``uint8`` or ``uint16``.

You can also get information about images without loading them using
:py:func:`bob.io.base.peek`:

.. doctest::

   >>> bob.io.base.peek(path_to_image)
   (dtype('uint8'), (3, 600, 512), (307200, 512, 1))

In order to visualize the loaded image you can use
:py:func:`bob.io.image.imshow`:

.. doctest::

  >>> img = bob.io.base.load(path_to_image)
  >>> bob.io.image.imshow(img)  # doctest: +SKIP

.. plot::

   import bob.io.base
   import bob.io.image
   from bob.io.base import test_utils

   path = test_utils.datafile('grace_hopper.png', 'bob.io.image')
   img = bob.io.base.load(path)
   bob.io.image.imshow(img)

Or you can just get a view (not copy) of your image that is
:py:mod:`matplotlib.pyplot` compatible using
:py:func:`bob.io.image.to_matplotlib`:

.. doctest::

  >>> img_view_for_matplotlib = bob.io.image.to_matplotlib(img)
  >>> assert img_view_for_matplotlib.shape[-1] == 3
  >>> assert img_view_for_matplotlib.base is img

You can also get the original image back using :py:func:`bob.io.image.to_bob`.


.. testcleanup:: *

  import shutil
  os.chdir(current_directory)
  shutil.rmtree(temp_dir)
