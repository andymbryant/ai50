import unittest
from parser import *
import os
import nltk
import sys
import re
import subprocess

cwd = os.getcwd()
filenames = os.listdir(cwd + '/sentences')

class ParserTest(unittest.TestCase):
    def setup(self):
        self.a = sys.argv[1]
        self.b = sys.argv[2]

    def test_parser(self):
        # print(sys.argv)
        for filename in filenames:
            print(filename)
            # result = subprocess.call("python parser.py " + cwd + '/sentences/' + filename)
            # print(result)
        # for filenames in files:
            result = main()
            print(result)
        # self.assertEqual(1, 1)

if __name__ == '__main__':
    # print(sys.argv)
    # sys.argv[1] = 'parser.py'
    # sys.argv[2] = 'sentences/10.txt'
    unittest.main()