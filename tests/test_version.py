"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import importlib
import logging
import numpy as np
import os
from parameterized import parameterized
from PIL import Image
import sys
import tempfile
import unittest

import pnglib
# from _defs import ALL_VERSIONS, LIBJPEG_VERSIONS


class TestVersion(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.original_version = pnglib.version.get()
        self.tmp = tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False)
        self.tmp.close()

    def tearDown(self):
        os.remove(self.tmp.name)
        del self.tmp
        pnglib.version.set(self.original_version)

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

    def test_set_version(self):
        """Test version set statement."""
        self.logger.info("test_set_version")
        # default version
        pnglib.version.set('1_6_37')
        self.assertEqual(pnglib.version.get(), '1_6_37')
        # set new version
        pnglib.version.set('1_6_39')
        self.assertEqual(pnglib.version.get(), '1_6_39')
        # default version
        pnglib.version.set('1_6_37')
        self.assertEqual(pnglib.version.get(), '1_6_37')


