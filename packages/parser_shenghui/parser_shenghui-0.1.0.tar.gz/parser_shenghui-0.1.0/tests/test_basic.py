# -*- coding: utf-8 -*-

from parser import Parser
from .context import TEST_DATA_DIR_PATH

import unittest
import os


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    def setUp(self):
        self.file_path = os.path.join(TEST_DATA_DIR_PATH, 'original_sample.txt')
        self.parser = Parser()
        self.parser.scan_document(self.file_path)

    def test_when_x_is_zero_and_then_three(self):
        self.assertEqual(len(self.parser.x_largest(0)), 0)
        self.assertCountEqual(self.parser.x_largest(3), ['1426828028','1426828056','1426828066'])


if __name__ == '__main__':
    unittest.main()
