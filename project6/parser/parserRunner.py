import unittest
from unittest.mock import patch
from parser import main
import os
import sys
import glob

# Not intended as a true test case
# This is a simple runner that shows all output immediately

class ParserTest(unittest.TestCase):
    def test_parser(self):
        filepath = os.getcwd() + '/sentences/*.txt'
        filenames = glob.glob(filepath)[::-1]
        for filename in filenames:
            test_argv = ["parser.py", filename]
            with patch.object(sys, 'argv', test_argv):
                main()

if __name__ == '__main__':
    unittest.main()