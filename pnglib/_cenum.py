"""Module with C-enumerations.

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

from __future__ import annotations
from dataclasses import dataclass
import enum


class _Enum(enum.Enum):
    """"""
    def __int__(self):
        """"""
        return self.value

    def __str__(self):
        """"""
        return self.name

    def __repr__(self):
        """"""
        return self.name


@dataclass
class Colortype(_Enum):
    """Representation of color space.

    Carries information about number of channels.
    """
    PNG_COLOR_TYPE_GRAY = 0
    """Y"""
    PNG_COLOR_TYPE_RGB = 2
    """RGB"""
    PNG_COLOR_TYPE_GRAY_ALPHA = 4
    PNG_COLOR_TYPE_GA = 4
    """Y+A"""
    PNG_COLOR_TYPE_PALETTE = 5
    """RGB palette"""
    PNG_COLOR_TYPE_RGB_ALPHA = 6
    PNG_COLOR_TYPE_RGBA = 6
    """RGB+A"""

    @property
    def channels(self) -> int:
        """Number of channels that the color space has."""
        channel_no = {
            "PNG_COLOR_TYPE_GRAY": 1,
            "PNG_COLOR_TYPE_PALETTE": 1,
            "PNG_COLOR_TYPE_GRAY_ALPHA": 2,
            "PNG_COLOR_TYPE_GA": 2,
            "PNG_COLOR_TYPE_RGB": 3,
            "PNG_COLOR_TYPE_RGB_ALPHA": 4,
            "PNG_COLOR_TYPE_RGBA": 4,
        }
        return channel_no[self.name]

    # must define, dataclass changes this
    def __repr__(self):
        """"""
        return self.name


@dataclass
class Transform(_Enum):
    PNG_TRANSFORM_IDENTITY = 0x0000  # rw
    """No transformation"""
    PNG_TRANSFORM_STRIP_16 = 0x0001  # ro
    """Strip 16-bit samples to 8-bits"""
    PNG_TRANSFORM_STRIP_ALPHA = 0x0002  # ro
    """Discard the alpha channel"""
    PNG_TRANSFORM_PACKING = 0x0004  # rw
    """Expand 1, 2 and 4-bit samples to bytes"""
    PNG_TRANSFORM_PACKSWAP = 0x0008  # rw
    """Change order of packed pixels to LSB first"""
    PNG_TRANSFORM_EXPAND = 0x0010  # ro
    """Perform set_expand()"""
    PNG_TRANSFORM_INVERT_MONO = 0x0020  # rw
    """Invert monochrome images"""
    PNG_TRANSFORM_SHIFT = 0x0040  # rw
    """Normalize pixels to the sBIT depth"""
    PNG_TRANSFORM_BGR = 0x0080  # rw
    """Flip RGB to BGR, RGBA to BGRA"""
    PNG_TRANSFORM_SWAP_ALPHA = 0x0100  # rw
    """Flip RGBA to ARGB or GA to AG"""
    PNG_TRANSFORM_SWAP_ENDIAN = 0x0200  # rw
    """Byte-swap 16-bit samples"""
    PNG_TRANSFORM_INVERT_ALPHA = 0x0400  # rw
    """Change alpha from opacity to transparency"""
    PNG_TRANSFORM_STRIP_FILLER = 0x0800  # wo
    """"""
    # libpng-1.2.34
    PNG_TRANSFORM_STRIP_FILLER_BEFORE = 0x0800  # wo
    """"""
    PNG_TRANSFORM_STRIP_FILLER_AFTER = 0x1000  # wo
    """"""
    # libpng-1.4.0
    PNG_TRANSFORM_GRAY_TO_RGB = 0x2000  # ro
    """"""
    # libpng-1.5.4
    PNG_TRANSFORM_EXPAND_16 = 0x4000  # ro
    """"""
    PNG_TRANSFORM_SCALE_16 = 0x8000  # ro
    """"""

    # must define, dataclass changes this
    def __repr__(self):
        """"""
        return self.name


@dataclass
class Interlace(_Enum):
    """interlacing type"""
    PNG_INTERLACE_NONE = 0
    """non-interlaced image"""
    PNG_INTERLACE_ADAM7 = 1
    """adam7 interlacing"""
    PNG_INTERLACE_LAST = 2
    """not a valid value"""

    # must define, dataclass changes this
    def __repr__(self):
        """"""
        return self.name


"""
/* This is for compression type. PNG 1.0-1.2 only define the single type. */
#define PNG_COMPRESSION_TYPE_BASE 0 /* Deflate method 8, 32K window */
#define PNG_COMPRESSION_TYPE_DEFAULT PNG_COMPRESSION_TYPE_BASE

/* This is for filter type. PNG 1.0-1.2 only define the single type. */
#define PNG_FILTER_TYPE_BASE      0 /* Single row per-byte filtering */
#define PNG_INTRAPIXEL_DIFFERENCING 64 /* Used only in MNG datastreams */
#define PNG_FILTER_TYPE_DEFAULT   PNG_FILTER_TYPE_BASE

/* These are for the oFFs chunk.  These values should NOT be changed. */
#define PNG_OFFSET_PIXEL          0 /* Offset in pixels */
#define PNG_OFFSET_MICROMETER     1 /* Offset in micrometers (1/10^6 meter) */
#define PNG_OFFSET_LAST           2 /* Not a valid value */

/* These are for the pCAL chunk.  These values should NOT be changed. */
#define PNG_EQUATION_LINEAR       0 /* Linear transformation */
#define PNG_EQUATION_BASE_E       1 /* Exponential base e transform */
#define PNG_EQUATION_ARBITRARY    2 /* Arbitrary base exponential transform */
#define PNG_EQUATION_HYPERBOLIC   3 /* Hyperbolic sine transformation */
#define PNG_EQUATION_LAST         4 /* Not a valid value */

/* These are for the sCAL chunk.  These values should NOT be changed. */
#define PNG_SCALE_UNKNOWN         0 /* unknown unit (image scale) */
#define PNG_SCALE_METER           1 /* meters per pixel */
#define PNG_SCALE_RADIAN          2 /* radians per pixel */
#define PNG_SCALE_LAST            3 /* Not a valid value */

/* These are for the pHYs chunk.  These values should NOT be changed. */
#define PNG_RESOLUTION_UNKNOWN    0 /* pixels/unknown unit (aspect ratio) */
#define PNG_RESOLUTION_METER      1 /* pixels/meter */
#define PNG_RESOLUTION_LAST       2 /* Not a valid value */

/* These are for the sRGB chunk.  These values should NOT be changed. */
#define PNG_sRGB_INTENT_PERCEPTUAL 0
#define PNG_sRGB_INTENT_RELATIVE   1
#define PNG_sRGB_INTENT_SATURATION 2
#define PNG_sRGB_INTENT_ABSOLUTE   3
#define PNG_sRGB_INTENT_LAST       4 /* Not a valid value */

/* This is for text chunks */
#define PNG_KEYWORD_MAX_LENGTH     79

/* Maximum number of entries in PLTE/sPLT/tRNS arrays */
#define PNG_MAX_PALETTE_LENGTH    256
"""
