#!/usr/bin/env python3

import logging
import unittest

from Text import Text

class TestTextFunctions(unittest.TestCase):

    def setUp(self):
        self.filename = "test_text.txt"
        
    def tearDown(self):
        del self.filename


if __name__ == '__main__':
    unittest.main()