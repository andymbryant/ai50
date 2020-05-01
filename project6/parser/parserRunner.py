import unittest
from unittest.mock import patch
from parser import main
import os
import sys
import glob

class ParserTest(unittest.TestCase):
    '''
    Runs the parser on each file in the sentences directory. This is not intended as a true test case,
    but rather as a way to review parser performance with each text file quickly.
    '''
    def test_parser(self):
        filepath = os.getcwd() + '/sentences/*.txt'
        # Get all filenames and reverse list to run sequentially
        filenames = glob.glob(filepath)[::-1]
        # Loop through filenames and add them to argv sequentially
        for filename in filenames:
            test_argv = ["parser.py", filename]
            with patch.object(sys, 'argv', test_argv):
                # Run main and check output
                main()

if __name__ == '__main__':
    unittest.main()