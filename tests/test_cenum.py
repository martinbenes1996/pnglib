"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import logging
import os
from parameterized import parameterized
import tempfile
import unittest

import pnglib


class TestCEnum(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.original_version = pnglib.version.get()
        self.tmp = tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False)
        self.tmp.close()

    def tearDown(self):
        os.remove(self.tmp.name)
        del self.tmp
        pnglib.version.set(self.original_version)