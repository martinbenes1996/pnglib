Glossary
===================================

This part briefly explains the concepts behind the library.
The rest of documentation will refer to this page as a knowledge base.

.. contents:: Table of Contents
   :local:
   :depth: 1

PNG file
--------

Details of PNG file.

PNG starts with 8B signature sequence: b'\x89PNG\x0d\x0a\x1a\x0a'.

The rest of the file consists of chunks.

Chunk consists of

* 4B length
* 4B type
* up to 2GB data
* 4B CRC value

Types of chunks are

* IHDR = basic information (width, height, bitdepth, color type, interlacing)
* PLTE = palette
* IDAT = compressed image data
* IEND = end chunk

* cHRM = primary chromaticities
* gAMA = used gamma correction (already applied to the sample)
* iCCP = ICC prodile
* sBIT = significant bits in the original data
* sRGB = standard RGB color space
* bKGD = default background color
* hIST = frequency of each color in the color palette (PLTE)
* tRNS = simple transparency for palette
* pHYs = physical pixel dimension (pixels per unit, unit)
* sPLT = suggested palette
* tIME = time of the last modification
* iTXt = text information (title, author, description, copyright, creation time, software, disclaimer, warning, source, comment)
* tEXt = free textyal information with keyword (<80 bytes) and the text value
* zTXt = compressed text, better for larger amounts of text carried with the image


References
""""""""""

* `PNG Specification <http://www.libpng.org/pub/png/spec/1.2/>`_


Glossary terms
--------------

.. glossary::

    PNG
        Portable Network Graphics
