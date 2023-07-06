pnglib
===================================

**pnglib** is a Python package, envelope for the popular C library *pnglib*
for handling PNG files.

Currently almost all of the popular Python image libraries use *libpng* under the hood,
however do not expose the whole spectrum of parameters that libpng offers.
This and more is possible with **jpeglib**.

Reading pixels of PNG file is as simple as

>>> import pnglib
>>> im = pnglib.read_spatial("input.png")
>>> im.spatial


With **pnglib** you can choose a particular version of *libpng* to
work with. Currently supported are all *pnglib* versions from *1.6.37* and *1.6.39*.

>>> pnglib.version.set('1.6.39')
>>> im = pnglib.read_spatial("input.png")
>>> im.spatial

.. note::

   This project is under active development.
