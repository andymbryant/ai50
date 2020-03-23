import unittest
from crossword import *
from generate import *

class TestMethods(unittest.TestCase):
    def setup(self):
        self.crossword_0 = Crossword('data/structure0.txt', 'data/words0.txt')
        self.crossword_1 = Crossword('data/structure1.txt', 'data/words1.txt')
        self.crossword_2 = Crossword('data/structure2.txt', 'data/words2.txt')

    def test_enforce_node_consistency(self):
        crossword_0 = Crossword('data/structure0.txt', 'data/words0.txt')
        creator_0 = CrosswordCreator(crossword_0)
        creator_0.enforce_node_consistency()
        creator_0_flags = []
        for key, val in creator_0.domains.items():
            for word in val:
                flag = len(word) == key.length
                creator_0_flags.append(flag)
        self.assertEqual(all(creator_0_flags), True)

        crossword_1 = Crossword('data/structure1.txt', 'data/words1.txt')
        creator_1 = CrosswordCreator(crossword_1)
        creator_1.enforce_node_consistency()
        creator_1_flags = []
        for key, val in creator_1.domains.items():
            for word in val:
                flag = len(word) == key.length
                creator_1_flags.append(flag)
        self.assertEqual(all(creator_1_flags), True)

        crossword_2 = Crossword('data/structure2.txt', 'data/words2.txt')
        creator_2 = CrosswordCreator(crossword_2)
        creator_2.enforce_node_consistency()
        creator_2_flags = []
        for key, val in creator_2.domains.items():
            for word in val:
                flag = len(word) == key.length
                creator_2_flags.append(flag)
        self.assertEqual(all(creator_2_flags), True)


    def test_revise(self):
        pass

if __name__ == '__main__':
    unittest.main()