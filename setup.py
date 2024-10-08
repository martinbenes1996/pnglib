
import codecs
import glob
import os
from pathlib import Path
import re
import setuptools
import setuptools.command.build_ext
import shutil
import sys

# wheel builder
try:
    from wheel.bdist_wheel import bdist_wheel

    class bdist_wheel_abi3(bdist_wheel):
        def get_tag(self):
            python, abi, plat = super().get_tag()
            if python.startswith("cp"):
                return "cp38", "abi3", plat
            return python, abi, plat

    custom_bdist_wheel = {'bdist_wheel': bdist_wheel_abi3}
except ModuleNotFoundError:
    custom_bdist_wheel = {}

# versions
__version__ = os.environ.get('VERSION_NEW', '0.0.2')
libpng_versions = {
    '1_6_37': (None, 1637),
    '1_6_39': (None, 1639),
}

# requirements
try:
    with open('requirements.txt') as f:
        reqs = f.read().splitlines()
except FileNotFoundError:
    reqs = ['numpy']

# description
with codecs.open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

# add zlib (dependency)
zlib_path = 'pnglib/cpnglib/zlib'
zlib_cfiles = [str(s) for s in list(Path(zlib_path).rglob('*.c'))]
zlib_hfiles = [str(s) for s in list(Path(zlib_path).rglob('*.h'))]
# zlib_sfiles = [str(s) for s in list(Path(zlib_path).rglob('*.S'))]
# czlib = setuptools.Extension(
#     name=zlib_path,
#     library_dirs=[zlib_path],
#     include_dirs=[zlib_path],
#     # extra_objects=zlib_sfiles,
#     sources=zlib_cfiles,
#     headers=zlib_hfiles,
#     define_macros=[],
#     extra_compile_args=[] if sys.platform.startswith("win") else ["-fPIC", "-g"], # , '-std=gnu9'],
#     language='C++',
#     py_limited_api=True,
# )

# create version dependent extensions
cfiles, hfiles = {}, {}
cpnglib = {}
for v in libpng_versions:

    # name of C library
    rootlib = Path('src') / 'pnglib' / 'cpnglib'
    clib = rootlib / v

    # create missing
    package_name = 'libpng'
    with open(Path(clib) / 'vpng.h', 'w') as f:
        f.write('#include "png.h"')
    # shutil.copy(
    #     f'{clib}/scripts/pnglibconf.h.prebuilt',
    #     f'{clib}/pnglibconf.h',
    # )

    # get all files
    files = [
        f
        for d in [rootlib, clib]
        for f in glob.glob(str(d/'*'))
        if re.fullmatch(r'.*\.(c|h|cpp|hpp)', f)
    ]

    # # get all files
    # files = [str(s) for s in (
    #     list(Path(clib).rglob('*.c')) +
    #     list(Path(clib).rglob('*.h')) +
    #     list(Path(clib).rglob('*.cpp')) +
    #     list(Path(clib).rglob('*.hpp'))
    # )]
    # files = [
    #     f'{clib}/{f}'
    #     for f in (
    #         list(Path(clib).rglob('*.c')) +
    #         list(Path(clib).rglob('*.h'))
    #     )
    #     for d in ['.', 'arm']
    #     for f in os.listdir(f'{clib}/{d}')
    #     if re.fullmatch(r'.*\.(c|h)', f)
    # ]
    # exclude files
    for excluded_module in [
        # platform dependents
        'android-ndk', 'linux-auxv', 'linux',
        'windows', 'rpng-win', 'rpng2-win',
        'linux_aux',
        # executables
        'intprefix', 'prefix', 'sym', 'symbols',
        'vers',
        # defines
        'def', 'intprefix',
        # file formats
        'readpng', 'readppm',
        'rpng-x', 'rpng2-x',
        'wpng', 'PngFile', 'VisualPng',
        # zlib
        'zfstream', 'android-ndk',
        # tests
        'tarith', 'pngstest',
    ]:
        lim = -2 - len(excluded_module)
        files = [f for f in files if f[lim:-2] != excluded_module]
        # files = [f for f in files if not f.startswith(excluded_module)]  # f.split('.')[0] != excluded_module]
    # print(files)
    # exit()

    # split to sources and headers
    cfiles[v] = [
        f for f in files
        if any(f.endswith(s) for s in ['c', '.cpp'])
    ]
    hfiles[v] = [
        f for f in files
        if f[-2:] == '.h'
    ]
    sources = cfiles[v]

    # # split to sources and headers
    # cfiles[v] = [f for f in files if f[-2:] == '.c']
    # hfiles[v] = [f for f in files if f[-2:] == '.h']
    # sfiles[v] = [f for f in files if f[-2:] == '.S']
    # cfiles[v].append('pnglib/cpnglib/cpnglib_spatial.cpp')
    # cfiles[v].append('pnglib/cpnglib/cpnglib_common.cpp')
    # cfiles[v].append('pnglib/cpnglib/cpnglib_common_texts.cpp')
    # hfiles[v].append('pnglib/cpnglib/cjpeglib.h')

    # define macros
    macros = [
        ('PNG_ZLIB_VERNUM', 0),
        ('PNG_DEBUG', 1),
        # ('PNG_ARM_NEON_INTRINSICS_AVAILABLE', 0),
        ('PNG_ARM_NEON_IMPLEMENTATION', 0),
        ('PNG_ARM_NEON_OPT', 0),
        ('PNG_MIPS_MSA_OPT', 0),
        ('PNG_INTEL_SSE_IMPLEMENTATION', 0)
    ]

    # define the extension
    cpnglib[v] = setuptools.Extension(
        name=f'pnglib.cpnglib.cpnglib_{v}',
        library_dirs=['pnglib/cpnglib', f'{clib}'],  # , zlib_path],
        include_dirs=['pnglib/cpnglib', f'{clib}', f'{clib}/zlib-1_2_13'],
        # extra_objects=sfiles[v],
        sources=sources + zlib_cfiles,
        headers=hfiles[v] + zlib_hfiles,
        define_macros=macros,
        extra_compile_args=[] if sys.platform.startswith("win") else ["-fPIC", "-g"],
        # extra_link_args=['-lzlib'],
        # language='C++',
        py_limited_api=True,
    )


# extension builder
class custom_build_ext(setuptools.command.build_ext.build_ext):
    def get_export_symbols(self, ext):
        parts = ext.name.split(".")
        if parts[-1] == "__init__":
            initfunc_name = "PyInit_" + parts[-2]
        else:
            initfunc_name = "PyInit_" + parts[-1]

    def build_extensions(self):
        setuptools.command.build_ext.build_ext.build_extensions(self)
        setuptools.command.build_ext.build_ext.get_export_symbols = self.get_export_symbols


# define package
setuptools.setup(
    name='pnglib',
    version=__version__,
    author=u'Martin Beneš',
    author_email='martinbenes1996@gmail.com',
    description="Python envelope for the popular C library" +
                "libpng for handling PNG files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license='MPL',
    project_urls={
        "Homepage": "https://pypi.org/project/pnglib/",
        "Documentation": 'https://pnglib.readthedocs.io/en/latest/',
        "Source": "https://github.com/martinbenes1996/pnglib/",
    },
    keywords=['pnglib', 'png', 'libong', 'compression', 'decompression'],
    install_requires=reqs,
    package_dir={'': 'src'},
    package_data={'': ['data/*']},
    include_package_data=True,
    ext_modules=[cpnglib[v] for v in libpng_versions],
    cmdclass={
        "build_ext": custom_build_ext,
        **custom_bdist_wheel
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)