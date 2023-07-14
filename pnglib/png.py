"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import copy
import ctypes
import dataclasses
import numpy as np
import os
import tempfile
import typing
import warnings

from ._bind import CPngLib
from ._cenum import Colortype, Interlace, CompressionType, FilterType
from ._cstruct import Color

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
    gamma: float = None
    """"""
    png_interlace: Interlace = Interlace.PNG_INTERLACE_NONE
    """"""
    compression_type: CompressionType = CompressionType.PNG_COMPRESSION_TYPE_BASE
    """"""
    filter_type: FilterType = FilterType.PNG_FILTER_TYPE_BASE
    """"""
    palette: typing.List[Color] = dataclasses.field(default_factory=lambda: [])
    """"""
    hist: np.ndarray = None
    """histogram of usage of colors in the palette"""
    background: Color = None
    """"""
    cHRM: np.ndarray = None
    """primary chromaticities as white x/y, red x/y, green x/y, blue x/y"""
    spatial: np.ndarray
    """pixel data tensor"""

    def _alloc_spatial(self, channels: int = None):
        if channels is None:
            channels = self.color_space.channels
        return (((ctypes.c_ubyte * self.width) * self.height) * channels)()

    def load(
        self,
        # transforms: typing.List,
    ) -> np.ndarray:

        # allocate spatial
        spatial = self._alloc_spatial(self.png_color_type.channels)

        # write content into temporary file
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmp.write(self.content)
        tmp.flush()
        tmp.close()

        # call
        CPngLib.read_png_spatial(
            path=str(self.path),
            srcfile=tmp.name,
            spatial=spatial,
            # transforms=transforms
        )
        # clean up temporary file
        os.remove(tmp.name)
        # process
        self.spatial = (
            np.ctypeslib.as_array(spatial)
            .astype(np.ubyte)
            .reshape(self.height, -1, self.png_color_type.channels)
        )
        return self.spatial

    def read_spatial(self) -> np.ndarray:
        warnings.warn('read_spatial() is obsolete, use load()')
        return self.load()

    def write_spatial(
        self,
        path: str = None,
    ):
        """Writes a spatial image representation (i.e. RGB) to a file.

        :param path: Destination file name. If not given, source file is overwritten.
        :type path: str, optional

        :Example:

        >>> im = pnglib.read_spatial("input.png")
        >>> im.write_spatial("output.png")
        """  # noqa: E501
        # colorspace
        png_color_type = (ctypes.c_int*1)(
            int(self.png_color_type))
        # palette
        palette = self.c_palette()
        # path
        dstfile = path if path is not None else self.path
        if dstfile is None:
            raise IOError('no destination file specified')

        # process
        spatial = np.ctypeslib.as_ctypes(
            self.spatial.reshape(
                self.png_color_type.channels,
                self.height,
                self.width,
            ).astype('uint8')
        )
        # call
        CPngLib.write_png_spatial(
            dstfile=str(dstfile),
            spatial=spatial,
            image_dims=self.c_image_dims(),
            png_color_type=png_color_type,
            bit_depth=8,
            png_interlace=int(self.png_interlace),
            palette=palette,
            num_palette=len(self.palette),
        )

    @property
    def spatial(self) -> np.ndarray:
        if self._spatial is None:
            self.load()
        return self._spatial

    @spatial.setter
    def spatial(self, spatial: np.ndarray):
        self._spatial = spatial

    @property
    def channels(self) -> int:
        try:
            return self._png_color_type.channels
        except AttributeError:
            return None

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

    def c_palette(self):
        if not self.palette:
            return None
        pxs = [
            (ctypes.c_byte * self.png_color_type.colors)(*c.pixel())
            for c in self.palette
        ]
        return ((ctypes.c_byte*3)*len(pxs))(*pxs)

    def copy(self):
        """Create a deep copy of the JPEG object."""
        return copy.deepcopy(self)

    def free(self):
        """Free the allocated tensors."""
        del self._spatial

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
    _png_interlace = (ctypes.c_int*1)()
    _num_palette = (ctypes.c_int*1)()
    _palette = ((ctypes.c_byte*3)*256)()
    _compression_type = (ctypes.c_int*1)()
    _filter_type = (ctypes.c_int*1)()
    _background = (ctypes.c_int16*5)()
    _gamma = (ctypes.c_double*1)()
    _hist = (ctypes.c_int16*256)()
    _cHRM = (ctypes.c_double*8)()

    # call
    CPngLib.read_png_info(
        srcfile=str(path),
        image_dims=_image_dims,
        channels=_channels,
        bit_depth=_bit_depth,
        png_color_space=_png_color_type,
        png_interlace=_png_interlace,
        palette=_palette,
        num_palette=_num_palette,
        compression_type=_compression_type,
        filter_type=_filter_type,
        background=_background,
        gamma=_gamma,
        hist=_hist,
        cHRM=_cHRM,
    )
    # histogram
    hist = None
    if _hist[0] >= 0:
        hist = np.ctypeslib.as_array(_hist)
    # background
    background = None
    if _background[0] >= 0:
        background = Color(
            index=_background[0],
            red=_background[1],
            green=_background[2],
            blue=_background[3],
            gray=_background[4],
        )
    # cHRM
    cHRM = None
    if _cHRM[0] >= 0:
        cHRM = np.ctypeslib.as_array(_cHRM)
    # create jpeg
    return PNG(
        path=str(path),
        content=None,
        height=_image_dims[0],
        width=_image_dims[1],
        png_color_type=Colortype(_png_color_type[0]),
        png_interlace=Interlace(_png_interlace[0]),
        compression_type=CompressionType(_compression_type[0]),
        filter_type=FilterType(_filter_type[0]),
        hist=hist,
        gamma=_gamma[0] if _gamma[0] >= 0 else None,
        background=background,
        cHRM=cHRM,
    )
