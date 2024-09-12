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
from ._cenum import Colortype, BitDepth, Interlace, CompressionType, FilterType, Transform, TextCompression, TextKeyword
from ._cstruct import Color
# from ._marker import Marker
# cenum abbreviations
PNG_COLOR_TYPE_GRAY = Colortype.PNG_COLOR_TYPE_GRAY
PNG_COLOR_TYPE_GRAY_ALPHA = Colortype.PNG_COLOR_TYPE_GRAY_ALPHA
PNG_COLOR_TYPE_RGB = Colortype.PNG_COLOR_TYPE_RGB
PNG_COLOR_TYPE_RGB_ALPHA = Colortype.PNG_COLOR_TYPE_RGB_ALPHA
PNG_COLOR_TYPE_PALETTE = Colortype.PNG_COLOR_TYPE_PALETTE
PNG_BIT_DEPTH_1 = BitDepth.PNG_BIT_DEPTH_1
PNG_BIT_DEPTH_2 = BitDepth.PNG_BIT_DEPTH_2
PNG_BIT_DEPTH_4 = BitDepth.PNG_BIT_DEPTH_4
PNG_BIT_DEPTH_8 = BitDepth.PNG_BIT_DEPTH_8
PNG_BIT_DEPTH_16 = BitDepth.PNG_BIT_DEPTH_16
PNG_TRANSFORM_IDENTITY = Transform.PNG_TRANSFORM_IDENTITY
PNG_TRANSFORM_STRIP_16 = Transform.PNG_TRANSFORM_STRIP_16
PNG_TRANSFORM_STRIP_ALPHA = Transform.PNG_TRANSFORM_STRIP_ALPHA
PNG_TRANSFORM_PACKING = Transform.PNG_TRANSFORM_PACKING
PNG_TRANSFORM_PACKSWAP = Transform.PNG_TRANSFORM_PACKSWAP
PNG_TRANSFORM_EXPAND = Transform.PNG_TRANSFORM_EXPAND
PNG_TRANSFORM_INVERT_MONO = Transform.PNG_TRANSFORM_INVERT_MONO
PNG_TRANSFORM_SHIFT = Transform.PNG_TRANSFORM_SHIFT
PNG_TRANSFORM_BGR = Transform.PNG_TRANSFORM_BGR
PNG_TRANSFORM_SWAP_ALPHA = Transform.PNG_TRANSFORM_SWAP_ALPHA
PNG_TRANSFORM_SWAP_ENDIAN = Transform.PNG_TRANSFORM_SWAP_ENDIAN
PNG_TRANSFORM_INVERT_ALPHA = Transform.PNG_TRANSFORM_INVERT_ALPHA
PNG_TRANSFORM_STRIP_FILLER = Transform.PNG_TRANSFORM_STRIP_FILLER
PNG_TRANSFORM_STRIP_FILLER_BEFORE = Transform.PNG_TRANSFORM_STRIP_FILLER_BEFORE
PNG_TRANSFORM_STRIP_FILLER_AFTER = Transform.PNG_TRANSFORM_STRIP_FILLER_AFTER
PNG_TRANSFORM_GRAY_TO_RGB = Transform.PNG_TRANSFORM_GRAY_TO_RGB
PNG_TRANSFORM_EXPAND_16 = Transform.PNG_TRANSFORM_EXPAND_16
PNG_TRANSFORM_SCALE_16 = Transform.PNG_TRANSFORM_SCALE_16
PNG_INTERLACE_NONE = Interlace.PNG_INTERLACE_NONE
PNG_INTERLACE_ADAM7 = Interlace.PNG_INTERLACE_ADAM7
# PNG_INTERLACE_LAST = Interlace.PNG_INTERLACE_LAST
PNG_COMPRESSION_TYPE_BASE = CompressionType.PNG_COMPRESSION_TYPE_BASE
PNG_COMPRESSION_TYPE_DEFAULT = CompressionType.PNG_COMPRESSION_TYPE_DEFAULT
PNG_FILTER_TYPE_BASE = FilterType.PNG_FILTER_TYPE_BASE
PNG_INTRAPIXEL_DIFFERENCING = FilterType.PNG_INTRAPIXEL_DIFFERENCING
PNG_FILTER_TYPE_DEFAULT = FilterType.PNG_FILTER_TYPE_DEFAULT
PNG_TEXT_COMPRESSION_UNKNOWN = TextCompression.PNG_TEXT_COMPRESSION_UNKNOWN
PNG_TEXT_COMPRESSION_NONE = TextCompression.PNG_TEXT_COMPRESSION_NONE
PNG_TEXT_COMPRESSION_zTXt_WR = TextCompression.PNG_TEXT_COMPRESSION_zTXt_WR
PNG_TEXT_COMPRESSION_NONE_WR = TextCompression.PNG_TEXT_COMPRESSION_NONE_WR
PNG_TEXT_COMPRESSION_zTXt = TextCompression.PNG_TEXT_COMPRESSION_zTXt
PNG_ITXT_COMPRESSION_NONE = TextCompression.PNG_ITXT_COMPRESSION_NONE
PNG_ITXT_COMPRESSION_zTXt = TextCompression.PNG_ITXT_COMPRESSION_zTXt
PNG_TEXT_KEY_TITLE = TextKeyword.PNG_TEXT_KEY_TITLE
PNG_TEXT_KEY_AUTHOR = TextKeyword.PNG_TEXT_KEY_AUTHOR
PNG_TEXT_KEY_DESCRIPTION = TextKeyword.PNG_TEXT_KEY_DESCRIPTION
PNG_TEXT_KEY_COPYRIGHT = TextKeyword.PNG_TEXT_KEY_COPYRIGHT
PNG_TEXT_KEY_CREATION_TIME = TextKeyword.PNG_TEXT_KEY_CREATION_TIME
PNG_TEXT_KEY_SOFTWARE = TextKeyword.PNG_TEXT_KEY_SOFTWARE
PNG_TEXT_KEY_DISCLAIMER = TextKeyword.PNG_TEXT_KEY_DISCLAIMER
PNG_TEXT_KEY_WARNING = TextKeyword.PNG_TEXT_KEY_WARNING
PNG_TEXT_KEY_SOURCE = TextKeyword.PNG_TEXT_KEY_SOURCE
PNG_TEXT_KEY_COMMENT = TextKeyword.PNG_TEXT_KEY_COMMENT
PNG_TEXT_KEY_UNKNOWN = TextKeyword.PNG_TEXT_KEY_UNKNOWN

# libjpeg versions
from .version import version

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