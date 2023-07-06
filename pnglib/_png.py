"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import copy
import ctypes
import dataclasses
import numpy as np
from typing import List, Dict, Union

from ._bind import CPngLib
from ._cenum import Colortype

# from ._cenum import Colorspace, MarkerType
# from ._huffman import Huffman
# from ._marker import Marker
# from ._notations import Jab_to_factors



@dataclasses.dataclass
class PNG:
    """PNG instance to work in spatial domain."""
    path: str
    """path to the png file"""
    content: bytes
    """cached binary content of the png"""
    height: int
    """image height"""
    width: int
    """image width"""
    png_color_type: Colortype
    """color space of the PNG file"""

    def _alloc_spatial(self, channels: int = None):
        if channels is None:
            channels = self.color_space.channels
        return (((ctypes.c_ubyte * self.width) * self.height) * channels)()

    @property
    def has_alpha(self) -> bool:
        """Indicator of presence of alpha channel.

        :return: True for color image, False for grayscale image
        :rtype: bool

        :Example:

        >>> im = jpeglib.read_spatial("input.png")
        >>> im.has_alpha # -> True

        >>> im = jpeglib.read_spatial(
        ...     "input.jpeg",
        ...     jpeglib.PNG_COLOR_TYPE_RGBA)
        >>> im.has_alpha # -> False

        """
        return self.num_components > 3

    @property
    def num_components(self) -> int:
        """Getter of number of color components in the PNG.

        :return: Number of color components.
        :rtype: bool

        :Example:

        >>> im = jpeglib.read_spatial("input.png")
        >>> im.num_components # -> 3

        >>> im = jpeglib.read_spatial(
        ...     "input.jpeg",
        ...     jpeglib.PNG_COLOR_TYPE_RGBA)
        >>> im.num_components # -> 4
        """
        return self.png_color_type.channels

    def c_image_dims(self):
        return (ctypes.c_int * 2)(self.height, self.width)

    def copy(self):
        """Create a deep copy of the JPEG object."""
        return copy.deepcopy(self)

    def free(self):
        """Free the allocated tensors."""
        raise NotImplementedError

    def close(self):
        """Closes the object. Defined for interface compatibility with PIL.

        :Example:

        >>> im = jpeglib.read_dct("input.jpeg")
        >>> # work with im
        >>> im.close()
        """
        pass

    def __enter__(self):
        """Method for using ``with`` statement together with :class:`JPEG`.

        :Example:

        >>> with jpeglib.read_dct("input.jpeg") as im:
        >>>     im.Y; im.Cb; im.Cr; im.qt
        """
        return self

    def __exit__(self, exception_type, exception_val, trace):
        """Method for using ``with`` statement together with :class:`JPEG`."""
        self.close()


def load_jpeg_info(path: str) -> PNG:
    """"""
    # allocate
    _image_dims = (ctypes.c_int*2)()
    _png_color_type = (ctypes.c_int*2)()
    _channels = (ctypes.c_int*1)()
    _bit_depth = (ctypes.c_int*1)()

    # call
    CPngLib.read_png_info(
        srcfile=str(path),
        image_dims=_image_dims,
        channels=_channels,
        bit_depth=_bit_depth,
        png_color_space=_png_color_type,
    )
    # process
    # num_components = _num_components[0]  # number of components in JPEG

    # create jpeg
    return PNG(
        path=str(path),
        content=None,
        height=_image_dims[0],
        width=_image_dims[1],
        png_color_type=Colortype(_png_color_type[0]),
    )
