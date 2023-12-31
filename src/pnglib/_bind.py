"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import ctypes
import os
import pathlib
import re

from . import cpnglib


class CPngLib:
    """"""

    @classmethod
    def png_lib_version(cls):
        return cls.get().png_lib_version()

    @classmethod
    def read_png_info(
        cls,
        srcfile: str,
        image_dims,
        channels,
        bit_depth,
        png_color_type,
        png_interlace,
        palette,
        num_palette,
        compression_type,
        num_text,
        max_text,
	    filter_type,
	    background,
	    gamma,
	    hist,
        cHRM,
    ):
        status = cls.get().read_png_info(
            cls.cstr(srcfile),
            image_dims,
            channels,
            bit_depth,
            png_color_type,
            png_interlace,
            palette,
            num_palette,
            compression_type,
            num_text,
            max_text,
            filter_type,
            background,
            gamma,
            hist,
            cHRM,
        )
        if status == 0:
            raise IOError(f"reading info of {srcfile} failed")

    @classmethod
    def read_png_texts(
        cls,
        srcfile: str,
	    num_text: int,
        max_text: int,
        text_compression,
	    text_keywords,
        text_lengths,
	    texts,
        path=None,
    ):
        if path is None:
            path = srcfile
        status = cls.get().read_png_texts(
            cls.cstr(srcfile),
            num_text,
            max_text,
            text_compression,
            text_keywords,
            text_lengths,
            texts,
        )
        if status == 0:
            raise IOError(f"reading of {path} texts failed")

    @classmethod
    def print_png_params(cls, srcfile: str):
        status = cls.get().print_png_params(cls.cstr(srcfile))
        if status == 0:
            raise IOError(f"reading of {srcfile} failed")

    @classmethod
    def read_png_spatial(
        cls,
        srcfile: str,
        spatial,
        path=None,
    ):
        if path is None:
            path = srcfile
        status = cls.get().read_png_spatial(
            cls.cstr(srcfile),
            spatial,
        )
        if status == 0:
            raise IOError(f"reading of {path} spatial failed")

    @classmethod
    def write_png_spatial(
        cls,
        dstfile: str,
        spatial,
        image_dims,
        png_color_type: int,
        bit_depth: int,
        png_interlace: int,
        palette,
        num_palette: int,
        num_text: int,
        text_compression,
        text_keywords,
        text_lengths,
        texts,
    ):
        status = cls.get().write_png_spatial(
            cls.cstr(dstfile),
            spatial,
            image_dims,
            png_color_type,
            bit_depth,
            png_interlace,
            palette,
            num_palette,
            num_text,
            text_compression,
            text_keywords,
            text_lengths,
            texts,
        )
        # text to latin-1
        if status == 0:
            raise IOError(f"writing spatial to {dstfile} failed")

    # MASKS = {
    #     "DO_FANCY_SAMPLING": (0b1 << 0),
    #     "DO_FANCY_UPSAMPLING": (0b1 << 0),
    #     "DO_FANCY_DOWNSAMPLING": (0b1 << 0),
    #     "DO_BLOCK_SMOOTHING": (0b1 << 2),
    #     "TWO_PASS_QUANTIZE": (0b1 << 4),
    #     "ENABLE_1PASS_QUANT": (0b1 << 6),
    #     "ENABLE_EXTERNAL_QUANT": (0b1 << 8),
    #     "ENABLE_2PASS_QUANT": (0b1 << 10),
    #     "OPTIMIZE_CODING": (0b1 << 12),
    #     "PROGRESSIVE_MODE": (0b1 << 14),
    #     "QUANTIZE_COLORS": (0b1 << 16),
    #     "ARITH_CODE": (0b1 << 18),
    #     "WRITE_JFIF_HEADER": (0b1 << 20),
    #     "WRITE_ADOBE_MARKER": (0b1 << 22),
    #     "CCIR601_SAMPLING": (0b1 << 24),
    #     "FORCE_BASELINE": (0b1 << 26),
    #     "TRELLIS_QUANT": (0b1 << 28),
    #     "TRELLIS_QUANT_DC": (0b1 << 30),
    # }

    # @classmethod
    # def flags_to_mask(cls, flags: List[str]):
    #     mask = 0xFFFFFFFF
    #     if flags is None:
    #         return mask
    #     for flag in flags:
    #         # parse sign
    #         sign = '-' if flag[0] == '-' else '+'
    #         if not flag[0].isalpha():
    #             flag = flag[1:]
    #         # get flags
    #         flagbit = cls.MASKS[flag.upper()]
    #         defbit = cls.MASKS[flag.upper()] << 1
    #         # map
    #         mask ^= defbit  # reset default value
    #         if sign == '-':
    #             mask ^= (flagbit)  # erase bit

    #     return ctypes.c_ulonglong(mask)

    # @classmethod
    # def mask_to_flags(cls, mask: int):
    #     flags = []
    #     bitmask = mask[0]
    #     # PROGRESSIVE_MODE = 0b00100
    #     # mask = ??1?? or ??0??
    #     if ((cls.MASKS["PROGRESSIVE_MODE"]) & bitmask) != 0:
    #         flags.append("PROGRESSIVE_MODE")

    #     return flags

    # @classmethod
    # def factor(cls, factor):
    #     if factor is None:
    #         factor = -1
    #     return ctypes.c_short(factor)

    _lib = None
    version = None

    @classmethod
    def get(cls):
        # connect to library
        if cls._lib is None:
            cls._lib = cls._bind_lib()
        # return library
        return cls._lib

    @classmethod
    def set_version(cls, version):
        cls._lib = cls._bind_lib(version=version)

    @classmethod
    def get_version(cls):
        return cls.version

    @classmethod
    def _versions(cls):
        so_files = [
            f
            for f in os.listdir(list(cpnglib.__path__)[0])
            if re.fullmatch(r'cpnglib_.*\.(.*\.so|pyd)', f)
        ]
        return so_files

    @classmethod
    def versions(cls):
        # list DLLs
        vs = [
            re.search(r'cpnglib_[^.]*\.(.*\.so|pyd)', f)[0]
            for f in cls._versions()
        ]
        # parse versions
        vs = [
            re.search(r'(?<=cpnglib_)[^.]*', f)[0]
            for f in cls._versions()
        ]
        return vs

    @classmethod
    def _bind_lib(cls, version='6b'):
        # path of the library
        so_files = [f for f in cls._versions() if re.fullmatch(
            f'cpnglib_{version}' + r'\.(.*\.so|pyd)', f)]
        try:
            so_file = so_files[0]
        except IndexError:
            so_file = None
        if so_file is None:
            raise RuntimeError(f'version "{version}" not found')
        libname = str(pathlib.Path(list(cpnglib.__path__)[0]) / so_file)
        # libname = str(os.path.join(list(cpnglib.__path__)[0], so_file))
        # connect
        cpnglib_dylib = ctypes.CDLL(libname)
        cls.version = version
        return cpnglib_dylib

    @staticmethod
    def cstr(s, encoding='utf-8'):
        if s is None:
            return None
        return ctypes.c_char_p(s.encode(encoding))
