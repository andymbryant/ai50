import unittest
import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

class TestTTTMethods(unittest.TestCase):

    def setUp(self):
        self.board_1 = [[EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.board_2 = [[EMPTY, EMPTY, O],
                        [EMPTY, X, EMPTY],
                        [X, EMPTY, EMPTY]]
        self.board_3 = [[O, X, O],
                        [X, O, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.board_4 = [[O, X, O],
                        [X, X, X],
                        [O, O, X]]
        self.board_5 = [[O, X, X],
                        [X, O, X],
                        [EMPTY, O, O]]
        self.board_6 = [[X, O, X],
                        [O, X, X],
                        [X, O, O]]
        self.board_7 = [[X, O, X],
                        [EMPTY, O, X],
                        [EMPTY, O, EMPTY]]

    def test_winner(self):
        # winner_1 = ttt.winner(self.board_1)
        # self.assertEqual(winner_1, None)

        # winner_2 = ttt.winner(self.board_2)
        # self.assertEqual(winner_2, None)

        # winner_3 = ttt.winner(self.board_3)
        # self.assertEqual(winner_3, None)

        # winner_4 = ttt.winner(self.board_4)
        # self.assertEqual(winner_4, X)

        # winner_5 = ttt.winner(self.board_5)
        # self.assertEqual(winner_5, O)

        # winner_6 = ttt.winner(self.board_6)
        # self.assertEqual(winner_6, X)

        winner_7 = ttt.winner(self.board_7)
        self.assertEqual(winner_7, O)


if __name__ == '__main__':
    unittest.main()
