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