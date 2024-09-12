"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import numpy as np
import typing
from ._cenum import Colortype, BitDepth


def png_color_type(
    num_components: int,
    palette: typing.List,
) -> Colortype:
    """Inferes png_color_type from number of channels."""
    # print(num_components, palette)
    if palette is not None:
        colortype = Colortype.PNG_COLOR_TYPE_PALETTE
    elif num_components == 3:
        colortype = Colortype.PNG_COLOR_TYPE_RGB
    elif num_components == 1:
        colortype = Colortype.PNG_COLOR_TYPE_GRAY
    elif num_components == 2:
        colortype = Colortype.PNG_COLOR_TYPE_GRAY_ALPHA
    elif num_components == 4:
        colortype = Colortype.PNG_COLOR_TYPE_RGB_ALPHA
    else:
        raise IOError('failed to infere colortype')
    return colortype


def bit_depth(
    spatial: np.ndarray,
) -> np.ndarray:
    """Inferes bit_depth from spatial."""
    if spatial.dtype == np.uint8:
        bitdepth = BitDepth.PNG_BIT_DEPTH_8
    elif spatial.dtype == np.uint16:
        bitdepth = BitDepth.PNG_BIT_DEPTH_16
    else:
        raise IOError('failed to infere bitdepth')
    return bitdepth
