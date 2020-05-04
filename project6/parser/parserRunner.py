import unittest
from unittest.mock import patch
from parser import preprocess, np_chunk, main, parser
import os
import sys
import glob

class ParserTest(unittest.TestCase):
    def test_preprocess(self):
        sentence_1 = "this is a Test sentence and it is4 254 fantastic."
        result_1 = preprocess(sentence_1)
        self.assertEqual(result_1, ['this', 'is', 'a', 'test', 'sentence', 'and', 'it', 'is4', 'fantastic'])

        sentence_2 = "I want to eat cake AND run through the forest?"
        result_2 = preprocess(sentence_2)
        self.assertEqual(result_2, ['i', 'want', 'to', 'eat', 'cake', 'and', 'run', 'through', 'the', 'forest'])

    def test_np_chunk(self):
        sentence_3 = 'Holmes lit a pipe.'
        proc_sent = preprocess(sentence_3)
        trees = list(parser.parse(proc_sent))
        chunks = []
        for tree in trees:
            for np in np_chunk(tree):
                chunk = " ".join(np.flatten())
                chunks.append(chunk)
        self.assertEqual(chunks, ['holmes', 'a pipe'])

    def test_parser(self):
        '''
        Runs the parser on each file in the sentences directory. This is not intended as a true test,
        but rather as a way to review parser performance with each text file quickly.
        '''
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