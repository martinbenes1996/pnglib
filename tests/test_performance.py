"""

Author: Martin Benes
Affiliation: Universitaet Innsbruck
"""

import logging
import numpy as np
import os
from scipy.stats import ttest_1samp
import timeit
import tempfile
import unittest

import pnglib


class TestPerformance(unittest.TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.original_version = pnglib.version.get()
        self.tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.tmp.close()

    def tearDown(self):
        os.remove(self.tmp.name)
        del self.tmp
        pnglib.version.set(self.original_version)