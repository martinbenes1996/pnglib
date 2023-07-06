"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

from ._cenum import Colortype


def png_color_type(
    num_components: int
) -> Colortype:
    """Inferes png_color_type from number of channels."""
    if num_components == 3:
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
