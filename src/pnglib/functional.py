"""Functional interface of the library.

Global functions to call.

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import numpy as np
import typing

from . import _infere
from . import png
from ._cenum import Colortype, Interlace, BitDepth
from ._cstruct import Color, Text


def read_spatial(
    path: str,
) -> png.PNG:
    """Function for decompressing the PNG.

    The file content is loaded once at the call.
    Then the operations are independent on the source file.

    :param path: Path to a source file in PNG format.
    :type path: str
    :return: PNG object
    :rtype: :class:`PNG`
    :raises [IOError]: When source file does not exist

    :Example:

    >>> im = pnglib.read_spatial("input.png")
    >>> im.spatial

    >>> try:
    >>>     im = pnglib.read_spatial("does_not_exist.png")
    >>> except IOError: # raised, file does not exist
    >>>     pass

    After call, only the parameters of PNG are read,
    so that it is known, how large buffer needs to be allocated.
    The allocation and reading of the data happens on the first query.

    >>> im = pnglib.read_spatial("input.png")
    >>> # at this point, internally im.spatial is None
    >>> # however on first query, it is read
    >>> print(im.spatial) # read and returned
    >>> print(im.spatial) # second time it is already stored in the object
    """  # noqa: E501
    # load file content
    path = str(path)
    with open(path, "rb") as f:
        content = f.read()
    # load info
    info = png.load_jpeg_info(path)

    # create jpeg
    im = png.PNG(
        path=path,
        content=content,
        height=info.height,
        width=info.width,
        png_color_type=info.png_color_type,
        bit_depth=info.bit_depth,
        png_interlace=info.png_interlace,
        spatial=None,
        palette=info.palette,
        texts=info._texts,  # load at init
        compression_type=info.compression_type,
        filter_type=info.filter_type,
        hist=info.hist,
    )
    return im


def from_spatial(
    spatial: np.ndarray,
    png_color_type: Colortype = None,
    png_interlace: Interlace = None,
    bit_depth: BitDepth = None,
    palette: typing.List[Color] = None,
    texts: typing.List[Text] = None,
) -> png.PNG:
    """A factory of :class:`PNG` from pixel data.

    The color type inference is based on number of color channels.
    For single channel, grayscale is assumed.
    For three channels, rgb is assumed.

    .. warning::
        Parameter :obj:`PNG.path` is not initialized.
        When calling :meth:`PNG.write_spatial`,
        you have to specify `path`,
        otherwise an error is raised.

    :param spatial: Spatial representation.
    :type spatial: np.ndarray
    :param png_color_type: Color type of the input. If not given, infered from the shape.
    :type png_color_type: str | Colortype, optional
    :raises [IOError]: When color type can't be infered.

    :Example:

    When data has three color channels (in the dimension 2), rgb is infered.

    >>> spatial = np.random.randint(0,255,(16,16,3),dtype=np.uint8)
    >>> im = pnglib.from_spatial(spatial) # 3 channels -> rgb infered
    >>> print(im.png_color_type) # -> Colortype.PNG_COLOR_TYPE_RGB
    >>> im.write_spatial("output.png")

    When data has one color channels, grayscale is infered

    >>> spatial = np.random.randint(0,255,(16,16,1),dtype=np.uint8)
    >>> im = pnglib.from_spatial(spatial) # 1 channel -> grayscale infered
    >>> print(im.png_color_type) # -> Colortype.PNG_COLOR_TYPE_GRAY
    >>> im.write_spatial("output.jpeg")

    For other color channels, color type can't be infered. Error is raised.

    >>> spatial = np.random.randint(0,255,(16,16,7),dtype=np.uint8)
    >>> try:
    >>>     im = pnglib.from_spatial(spatial)
    >>> except IOError:
    >>>     raised

    When output is not specified when writing, error is raised.

    >>> spatial = np.random.randint(0,255,(16,16,3),dtype=np.uint8)
    >>> im = pnglib.from_spatial(spatial)
    >>> try:
    >>>     im.write_spatial()
    >>> except IOError:
    >>>     pass
    """
    # shape
    height, width, num_components = spatial.shape
    # infere colorspace
    if png_color_type is None:
        png_color_type = _infere.png_color_type(num_components, palette)
    if png_color_type is Colortype.PNG_COLOR_TYPE_PALETTE:
        assert palette is not None, 'palette PNG with unspecified palette'
    # set non-given default
    if bit_depth is None:
        bit_depth = _infere.bit_depth(spatial)
    if bit_depth is not BitDepth.PNG_BIT_DEPTH_8:
        raise NotImplementedError('only bit depth 8 is supported for now')
    if png_interlace is None:
        png_interlace = Interlace.PNG_INTERLACE_NONE

    # create jpeg
    return png.PNG(
        path=None,
        content=None,
        height=height,
        width=width,
        png_color_type=png_color_type,
        bit_depth=bit_depth,
        png_interlace=png_interlace,
        palette=palette,
        texts=[] if texts is None else texts,
        spatial=spatial,
    )
