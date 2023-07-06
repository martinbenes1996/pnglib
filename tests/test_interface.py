"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import logging
import numpy as np
import os
from pathlib import Path
from PIL import Image
import tempfile
import unittest

import pnglib


class TestInterface(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.original_version = pnglib.version.get()
        self.tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.tmp.close()

    def tearDown(self):
        os.remove(self.tmp.name)
        del self.tmp
        pnglib.version.set(self.original_version)

    def test_read_spatial(self):
        self.logger.info("test_read_spatial")
        im = pnglib.read_spatial("examples/lizard.png")
        # inner state before reading
        self.assertEqual(im.path, "examples/lizard.png")  # source file
        self.assertTrue(im.content is not None)
        self.assertIsInstance(im.content, bytes)
        self.assertEqual(im.height, 512)
        self.assertEqual(im.width, 512)
        self.assertIsInstance(im.png_color_type, pnglib.Colortype)
        self.assertEqual(im.num_components, 3)
        # read spatial
        im.spatial
        # inner state after reading
        self.assertIsInstance(im.spatial, np.ndarray)
        self.assertEqual(len(im.spatial.shape), 3)
        self.assertEqual(im.spatial.shape[0], im.height)
        self.assertEqual(im.spatial.shape[1], im.width)
        self.assertEqual(im.spatial.shape[2], im.num_components)

    # def test_read_spatial_grayscale(self):
    #     self.logger.info("test_read_spatial_grayscale")
    #     # read info
    #     im = pnglib.read_spatial("examples/IMG_0791.jpeg",
    #                              pnglib.Colortype.PNG_COLOR_TYPE_GRAY)
    #     # inner state before reading
    #     self.assertEqual(im.path, "examples/IMG_0791.jpeg")  # source file
    #     self.assertTrue(im.content is not None)
    #     self.assertIsInstance(im.content, bytes)
    #     self.assertEqual(im.height, 3024)
    #     self.assertEqual(im.width, 4032)
    #     self.assertIsInstance(im.block_dims, np.ndarray)
    #     self.assertEqual(im.block_dims[0, 0], im.height//8)
    #     self.assertEqual(im.block_dims[0, 1], im.width//8)
    #     self.assertIsInstance(im.samp_factor, np.ndarray)
    #     self.assertEqual(im.samp_factor[0, 0], 2)
    #     self.assertEqual(im.samp_factor[0, 1], 2)
    #     self.assertIsInstance(im.jpeg_color_space, jpeglib.Colorspace)
    #     self.assertEqual(im.num_components, 1)
    #     self.assertEqual(im.channels, 1)
    #     self.assertEqual(len(im.markers), 2)
    #     # read spatial
    #     im.spatial
    #     # inner state after reading
    #     self.assertIsInstance(im.spatial, np.ndarray)
    #     self.assertEqual(len(im.spatial.shape), 3)
    #     self.assertEqual(im.spatial.shape[0], im.height)
    #     self.assertEqual(im.spatial.shape[1], im.width)
    #     self.assertEqual(im.spatial.shape[2], im.channels)

    def test_with_version(self):
        """Test with statement for version."""
        self.logger.info("test_with_version")
        # default version
        pnglib.version.set('1_6_37')
        self.assertEqual(pnglib.version.get(), '1_6_37')
        # block with new version
        with pnglib.version('1_6_39'):
            self.assertEqual(pnglib.version.get(), '1_6_39')
        # back to default
        self.assertEqual(pnglib.version.get(), '1_6_37')

    def test_pathlib(self):
        """Test path as pathlib.Path."""
        self.logger.info("test_pathlib")
        # open
        path = Path('examples/lizard.png')
        im = pnglib.read_spatial(path)
        # load
        im.load()
        # write
        im.write_spatial(Path(self.tmp.name))

    def test_read_pil(self):
        self.logger.info("test_read_pil")
        # read with PIL
        im = Image.open("examples/lizard.png")
        pilnpshape = np.array(im).shape
        pilsize = im.size
        # read dct
        im = pnglib.read_spatial("examples/lizard.png")
        # spatial
        self.assertEqual(im.spatial.shape[0], pilsize[1])
        self.assertEqual(im.spatial.shape[1], pilsize[0])
        self.assertEqual(im.spatial.shape[0], pilnpshape[0])
        self.assertEqual(im.spatial.shape[1], pilnpshape[1])

    def test_copy(self):
        self.logger.info("test_read_pil")
        # read DCT
        im = pnglib.read_spatial("examples/lizard.png")
        spatial_original = im.spatial.copy()
        # change spatial
        im2 = im.copy()
        im2.spatial[0, 0, 0] += 1
        # check unequal
        self.assertTrue((im.spatial == spatial_original).all())
        self.assertFalse((im.spatial == im2.spatial).all())


__all__ = ["TestInterface"]