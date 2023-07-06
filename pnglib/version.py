"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import ctypes
from typing import List
from ._bind import CPngLib


class version:
    """Class grouping functions for controlling libpng method."""

    @classmethod
    def set(cls, version: str):
        """Sets the version of libpng to use. Loads the library.

        :param version: libpng version, one of 1.6.37.
        :type version: str
        :raises [NotImplementedError]: unsupported libpng version

        :Example:

        >>> import pnglib
        >>> pnglib.version.set('16')
        """  # noqa: E501
        try:
            # libpng
            if version in {
                '1_6_37',
                '1_6_39',
            }:
                CPngLib.set_version(version=version)
            else:
                raise NotImplementedError(
                    f'Unsupported libjpeg version: {version}')
        except RuntimeError:
            raise RuntimeError(
                f'version "{version}" not found, '
                'was the package compiled correctly?'
            )

    @staticmethod
    def get() -> str:
        """Gets the currently used version of libpng.

        :return: libpng version or None if not been loaded yet.
        :rtype: str, None

        :Example:

        >>> import pnglib
        >>> pnglib.version.set('6b')
        >>> pnglib.version.get()
        '6b'
        """
        return CPngLib.get_version()

    @staticmethod
    def _png_lib_version() -> str:
        """Returns value of png_lib_version macro."""
        return CPngLib.jpeg_lib_version()

    @staticmethod
    def _get_lib() -> ctypes.CDLL:
        """Low-level getter of the dynamic library.

        :return: Dynamic library object or None if not loaded yet.
        :rtype: ctypes.CDLL, None
        """
        return CPngLib.get()

    @staticmethod
    def versions() -> List[str]:
        """Lists present DLLs of versions."""
        return CPngLib.versions()

    def __init__(self, version):
        """Constructor, used in with statement.

        :param version: Version to set inside with block.
        :type version: str
        """
        self.next = version

    def __enter__(self):
        """Sets new version in a block.

        :Example:

        >>> jpeglib.version.set('6b')
        >>> # working with 6b
        >>> # [...]
        >>> with jpeglib.version('8d'):
        >>>     # working with 8d
        >>>     # [...]
        >>>     pass
        """
        self.prev = self.get()
        self.set(self.next)

    def __exit__(self, *args, **kw):
        """Recovers a previous version, when exiting `with` block.

        :Example:

        >>> # working with 6b
        >>> # [...]
        >>> with jpeglib.version('8d'):
        >>>     # working with 8d
        >>>     # [...]
        >>>     pass
        >>> # working with 6b (again)
        >>> # [...]
        """
        self.set(self.prev)


__all__ = ['version']
