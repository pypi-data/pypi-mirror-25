.. vim: set fileencoding=utf-8 :
.. Manuel Gunther <siebenkopf@googlemail.com>
.. Mon May 23 15:25:41 MDT 2016

=========
 C++ API
=========

The C++ API of ``bob.io.image`` allows users to read and write images in different file formats.
For all image tyres, there exist two functions for reading and writing image, a function to peek the color information (if applicable) and a C++ class that can be used for more detailed information about the image.

Generic functions
-----------------

These functions read and write images based on the filename extension.
Currently, only ``uint8_t`` data type is supported (because this data type is supported by all of our codes).
For other data types, please use the specialized functions as described below.

.. code-block: cpp

   #include <bob.io.image/image.h>

.. cpp:function:: bool bob::io::image::is_color_image(const std::string& filename)

   Returns ``true`` if the image with the given name is a color image, else ``false``.
   It might raise an exception if the extension is not supported.

.. cpp:function:: blitz::Array<uint8_t,2> bob::io::image::read_gray_image(const std::string& filename)

   Reads a gray image.
   It might raise an exception if the extension is not supported.

.. cpp:function:: blitz::Array<uint8_t,3> bob::io::image::read_color_image(const std::string& filename)

   Reads a color image.
   It might raise an exception if the extension is not supported.

.. cpp:function:: void bob::io::image::write_gray_image(const blitz::Array<uint8_t,2>& image, const std::string& filename)

   Writes the gray ``image``.
   If the file exists, it will be overwritten.

.. cpp:function:: void bob::io::image::write_color_image(const blitz::Array<uint8_t,3>& image, const std::string& filename)

   Writes the color ``image``.
   If the file exists, it will be overwritten.


BMP
---

.. code-block: cpp

   #include <bob.io.image/bmp.h>

.. cpp:function:: blitz::Array<uint8_t,3> bob::io::image::read_bmp(const std::string& filename)

   Reads a color BMP image of data type ``uint8_t``.

.. cpp:function:: void bob::io::image::write_bmp(const blitz::Array<uint8_t,3>& image, const std::string& filename)

   Writes the BMP color ``image`` .
   If the file exists, it will be overwritten.
   Only ``uint8_t`` data type is supported.


GIF
---

.. code-block: cpp

   #include <bob.io.image/gif.h>

.. cpp:function:: blitz::Array<uint8_t,3> bob::io::image::read_gif(const std::string& filename)

   Reads a color GIF image of data type ``uint8_t``.

.. cpp:function:: void bob::io::image::write_gif(const blitz::Array<uint8_t,3>& image, const std::string& filename)

   Writes the GIF color ``image`` .
   If the file exists, it will be overwritten.
   Only ``uint8_t`` data type is supported.


JPEG
----

.. code-block: cpp

   #include <bob.io.image/jpeg.h>

.. cpp:function:: bool bob::io::image::is_color_jpeg(const std::string& filename)

   Returns ``true`` if the JPEG image with the given name is a color image, else ``false``.

.. cpp:function:: template <int N> blitz::Array<uint8_t,N> bob::io::image::read_jpeg(const std::string& filename)

   Reads a JPEG image of the given type (grayscale: ``N=2`` or color: ``N=3``).
   Only ``uint8_t`` data type is supported.
   Please assure that you read images of the correct color type, see :cpp:func:`bob::io::image::is_color_jpeg`.

.. cpp:function:: template <int N> void bob::io::image::write_jpeg(const blitz::Array<uint8_t,N>& image, const std::string& filename)

   Writes the JPEG ``image`` of the given type (grayscale: ``N=2`` or color: ``N=3``) to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` data type is supported.


TIFF
----

.. code-block: cpp

   #include <bob.io.image/tiff.h>

.. cpp:function:: bool bob::io::image::is_color_tiff(const std::string& filename)

   Returns ``true`` if the TIFF image with the given name is a color image, else ``false``.

.. cpp:function:: template <class T, int N> blitz::Array<T,N> bob::io::image::read_tiff(const std::string& filename)

   Reads a TIFF image of the given type (grayscale: ``N=2`` or color: ``N=3``).
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Please assure that you read images of the correct color type, see :cpp:func:`bob::io::image::is_color_tiff`.

.. cpp:function:: template <class T, int N> void bob::io::image::write_tiff(const blitz::Array<T,N>& image, const std::string& filename)

   Writes the TIFF ``image`` of the given type (grayscale: ``N=2`` or color: ``N=3``) to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.


PNG
---

.. code-block: cpp

   #include <bob.io.image/png.h>

.. cpp:function:: bool bob::io::image::is_color_png(const std::string& filename)

   Returns ``true`` if the PNG image with the given name is a color image, else ``false``.

.. cpp:function:: template <class T, int N> blitz::Array<T,N> bob::io::image::read_png(const std::string& filename)

   Reads a PNG image of the given type (grayscale: ``N=2`` or color: ``N=3``).
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Please assure that you read images of the correct color type, see :cpp:func:`bob::io::image::is_color_png`.

.. cpp:function:: template <class T, int N> void bob::io::image::write_png(const blitz::Array<T,N>& image, const std::string& filename)

   Writes the PNG ``image`` of the given type (grayscale: ``N=2`` or color: ``N=3``) to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.


NetPBM
------

.. note::
   Internally, the image IO is based on the filename extension to decide, which codec to use.
   Hence, the filename extension needs to match the function and data type that you use.
   Use ``.pbm`` for binary, ``.pgm`` for gray level images, and any other extension (typically ``.ppm``) for color images.

.. code-block: cpp

   #include <bob.io.image/netpbm.h>

.. cpp:function:: bool bob::io::image::is_color_p_m(const std::string& filename)

   Returns ``true`` if the image with the given name is a color image, else ``false``.

.. cpp:function:: template <class T, int N> blitz::Array<T,N> bob::io::image::read_p_m(const std::string& filename)

   Reads an image of the given type (grayscale: ``N=2`` or color: ``N=3``).
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Please assure that you read images of the correct color type, see :cpp:func:`bob::io::image::is_color_p_m`.

.. cpp:function:: template <class T, int N> void bob::io::image::write_p_m(const blitz::Array<T,N>& image, const std::string& filename)

   Writes the ``image`` of the given type (grayscale: ``N=2`` or color: ``N=3``) to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.


.. cpp:function:: template <class T> blitz::Array<T,2> bob::io::image::read_pbm(const std::string& filename)

   Reads an binary image.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Filename extension ``.pbm`` is required.

.. cpp:function:: template <class T> void bob::io::image::write_pbm(const blitz::Array<T,2>& image, const std::string& filename)

   Writes the binary ``image`` to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Filename extension ``.pbm`` is required.


.. cpp:function:: template <class T> blitz::Array<T,2> bob::io::image::read_pgm(const std::string& filename)

   Reads an grayscale image. Only ``uint8_`` and ``uint16_`` data types are supported.
   Filename extension ``.pgm`` is required.

.. cpp:function:: template <class T> void bob::io::image::write_pgm(const blitz::Array<T,2>& image, const std::string& filename)

   Writes the grayscale ``image`` to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Filename extension ``.pgm`` is required.


.. cpp:function:: template <class T> blitz::Array<T,3> bob::io::image::read_ppm(const std::string& filename)

   Reads an binary color image. Only ``uint8_`` and ``uint16_`` data types are supported.
   Filename extension cannot be ``.pbm`` or ``.pgm``.

.. cpp:function:: template <class T> void bob::io::image::write_ppm(const blitz::Array<T,3>& image, const std::string& filename)

   Writes the color ``image`` to a file with the given ``filename``.
   If the file exists, it will be overwritten.
   Only ``uint8_t`` and ``uint16_t`` data types are supported.
   Filename extension cannot be ``.pbm`` or ``.pgm``.

.. include:: links.rst
