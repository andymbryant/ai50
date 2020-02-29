import unittest
import pagerank as pr

DAMPING = 0.85
SAMPLES = 10_000

class TestPageRankMethods(unittest.TestCase):
    def setUp(self):
        self.corpus_0 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        self.corpus_1 = {"1.html": {}, "2.html": {"3.html"}, "3.html": {"1.html", "2.html"}}
        self.corpus_2 = {"2.html": {}, "3.html": {"2.html"}}

    def testTransitionModel(self):
        ranks_0 = pr.transition_model(self.corpus_0, "1.html", DAMPING)
        self.assertEqual(ranks_0, {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475})
        # Add method to check if all values add to 1

        ranks_1 = pr.transition_model(self.corpus_1, "1.html", DAMPING)
        self.assertEqual(ranks_1, {"1.html": 0.333, "2.html": 0.333, "3.html": 0.333})

        ranks_2 = pr.transition_model(self.corpus_2, "2.html", DAMPING)
        self.assertEqual(ranks_2, {"2.html": 0.500, "3.html": 0.500})

if __name__ == '__main__':
    unittest.main()