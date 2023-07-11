"""
Python envelope for the popular C library libpng for handling PNG files.

It offers full control over compression and decompression
and exposes PNG-specific compression parameters.

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

# functions
from .functional import read_spatial, from_spatial  # read_dct, read_spatial, from_spatial, from_dct

# # jpeg objects
# from .dct_jpeg import DCTJPEG, DCTJPEGio, to_jpegio
# from .spatial_jpeg import SpatialJPEG

# # cenums
from ._cenum import Colortype, Interlace
from ._cstruct import Color
# from ._marker import Marker
# cenum abbreviations
PNG_COLOR_TYPE_GRAY = Colortype.PNG_COLOR_TYPE_GRAY
PNG_COLOR_TYPE_GRAY_ALPHA = Colortype.PNG_COLOR_TYPE_GRAY_ALPHA
PNG_COLOR_TYPE_RGB = Colortype.PNG_COLOR_TYPE_RGB
PNG_COLOR_TYPE_RGB_ALPHA = Colortype.PNG_COLOR_TYPE_RGB_ALPHA
PNG_COLOR_TYPE_PALETTE = Colortype.PNG_COLOR_TYPE_PALETTE

# libjpeg versions
from .version import version

# # for unit tests
# from ._notations import Jab_to_factors

# package version
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution("pnglib").version
except pkg_resources.DistributionNotFound:
    __version__ = None

# set default version
try:
    version.set('1_6_37')
except IndexError:
    import logging
    logging.warning('found versions: ' + ' '.join(version.versions()))
    raise RuntimeError('invalid installation, version 1_6_37 not found')

__all__ = [
    # 'read_dct', 'read_spatial', 'from_spatial', 'from_dct', 'to_jpegio',
    # 'SpatialJPEG', 'DCTJPEG', 'DCTJPEGio',
    # 'Colorspace', 'DCTMethod', 'Dithermode', 'Marker', 'MarkerType',
    # 'version', 'Jab_to_factors',
    # '__version__',
]