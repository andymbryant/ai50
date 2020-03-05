import unittest
import pagerank as pr

DAMPING = 0.85
SAMPLES = 10_000

class TestPageRankMethods(unittest.TestCase):
    def setUp(self):
        self.corpus_0 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        self.corpus_1 = {"1.html": {}, "2.html": {"3.html"}, "3.html": {"1.html", "2.html"}}
        self.corpus_2 = {"2.html": {}, "3.html": {"2.html"}}
        self.corpus_3 = {"1.html": {"2.html", "3.html"}, "2.html": {"1.html", "3.html"}, "3.html": {"2.html"}}

    # def testTransitionModel(self):
    #     trans_model_0 = pr.transition_model(self.corpus_0, "1.html", DAMPING)
    #     self.assertEqual(trans_model_0, {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475})
    #     # Add method to check if all values add to 1

    #     trans_model_1 = pr.transition_model(self.corpus_1, "1.html", DAMPING)
    #     self.assertEqual(trans_model_1, {"1.html": 0.333, "2.html": 0.333, "3.html": 0.333})

    #     trans_model_2 = pr.transition_model(self.corpus_2, "2.html", DAMPING)
    #     self.assertEqual(trans_model_2, {"2.html": 0.500, "3.html": 0.500})

    def testIteratePagerank(self):
        pagerank_3 = pr.iterate_pagerank(self.corpus_3, DAMPING)
        self.assertEqual(pagerank_3, {'1.html': 0.232539658203125, '2.html': 0.43412700846354163, '3.html': 0.3333333333333333})

if __name__ == '__main__':
    unittest.main()