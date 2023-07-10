"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import ctypes
from dataclasses import dataclass
import numpy as np
import os
import tempfile
import warnings

from ._bind import CPngLib
from ._cenum import Colortype
from ._png import PNG


@dataclass
class SpatialPNG(PNG):
    """PNG instance to work in spatial domain."""
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
            )
        )
        # call
        CPngLib.write_png_spatial(
            dstfile=str(dstfile),
            spatial=spatial,
            image_dims=self.c_image_dims(),
            png_color_type=png_color_type,
            bit_depth=8,
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
    def png_color_type(self) -> np.ndarray:
        return self._png_color_type

    @png_color_type.setter
    def png_color_type(self, png_color_type: Colortype):
        self._png_color_type = png_color_type

    @property
    def channels(self) -> int:
        try:
            return self._png_color_type.channels
        except AttributeError:
            return None

    def free(self):
        """Free the allocated tensors."""
        del self._spatial
