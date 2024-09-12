"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import cv2
import logging
import numpy as np
import os
from parameterized import parameterized
from PIL import Image
import tempfile
import unittest

import pnglib
# from _defs import ALL_VERSIONS, version_cluster, qt50_standard


class TestSpatial(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.original_version = pnglib.version.get()
        self.tmp = tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False)
        self.tmp.close()

    def tearDown(self):
        os.remove(self.tmp.name)
        del self.tmp
        pnglib.version.set(self.original_version)

    def test_read_pil(self):
        """Test the same output as PIL."""
        self.logger.info("test_read_pil")
        # read with PIL
        im = Image.open("examples/lizard.png")
        pilnp = np.array(im)
        pilsize = im.size
        # read dct
        im = pnglib.read_spatial("examples/lizard.png")
        # spatial
        self.assertEqual(im.spatial.shape[0], pilsize[1])
        self.assertEqual(im.spatial.shape[1], pilsize[0])
        self.assertEqual(im.spatial.shape[0], pilnp.shape[0])
        self.assertEqual(im.spatial.shape[1], pilnp.shape[1])
        np.testing.assert_array_equal(im.spatial, pilnp)

    def test_read_cv2(self):
        """Test the same output as cv2."""
        self.logger.info("test_read_cv2")
        # read with PIL
        cv2bgr = cv2.imread("examples/lizard.png")
        cv2rgb = cv2bgr[..., -1::-1]
        cv2shape = cv2rgb.shape
        # read dct
        im = pnglib.read_spatial("examples/lizard.png")
        # spatial
        self.assertEqual(im.spatial.shape[0], cv2rgb.shape[0])
        self.assertEqual(im.spatial.shape[1], cv2rgb.shape[1])
        self.assertEqual(im.spatial.shape[2], cv2rgb.shape[2])
        np.testing.assert_array_equal(im.spatial, cv2rgb)

    def test_palette(self):
        """Test writing palette image."""
        self.logger.info('test_palette')
        # load image
        im = Image.open('examples/lizard.png').convert('L')
        x = np.array(im)[..., None]
        # create palette PNG
        palette = [
            # pnglib.Color(gray=v)
            pnglib.Color(red=v, green=v, blue=v)
            for v in range(256)
        ]
        im = pnglib.from_spatial(
            spatial=x,
            palette=palette,
        )
        # # print(im.png_color_type)
        # tmp_name = 'palette.png'
        # # write palette PNG
        # im.write_spatial(tmp_name)
        # # read palette PNG
        # im2 = pnglib.read_spatial(tmp_name)
        # im2.load()
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            # write palette PNG
            im.write_spatial(tmp.name)
            # read palette PNG
            im2 = pnglib.read_spatial(tmp.name)
            im2.load()
        # print(im2.palette)

        # print(x)
        # print(im)
