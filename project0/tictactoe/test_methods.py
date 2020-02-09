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

    def test_player(self):
        player_1 = ttt.player(self.board_1)
        self.assertEqual(player_1, X)

        self.player_2 = ttt.player(self.board_2)
        self.assertEqual(self.player_2, O)

        self.player_3 = ttt.player(self.board_3)
        self.assertEqual(self.player_3, X)

    def test_actions(self):
        actions_1 = ttt.actions(self.board_1)
        self.assertEqual(actions_1, {
                         (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)})

        actions_2 = ttt.actions(self.board_2)
        self.assertEqual(
            actions_2, {(0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2)})

        actions_3 = ttt.actions(self.board_3)
        self.assertEqual(actions_3, {(1, 2), (2, 0), (2, 1), (2, 2)})

    def test_result(self):
        action_1 = (1, 2)
        result_1 = ttt.result(self.board_1, action_1)
        self.assertEqual(
            result_1, [[EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, X],
                       [EMPTY, EMPTY, EMPTY]])

        action_2 = (2, 2)
        result_2 = ttt.result(self.board_2, action_2)
        self.assertEqual(
            result_2, [[EMPTY, EMPTY, O],
                       [EMPTY, X, EMPTY],
                       [X, EMPTY, O]])

        action_3 = (2, 0)
        result_3 = ttt.result(self.board_3, action_3)
        self.assertEqual(
            result_3, [[O, X, O],
                       [X, O, EMPTY],
                       [X, EMPTY, EMPTY]])

        action_4 = (0, 0)
        self.assertRaises(ValueError, ttt.result, self.board_3, action_4)

    def test_winner(self):
        winner_1 = ttt.winner(self.board_1)
        self.assertEqual(winner_1, None)

        winner_2 = ttt.winner(self.board_2)
        self.assertEqual(winner_2, None)

        winner_3 = ttt.winner(self.board_3)
        self.assertEqual(winner_3, None)

        winner_4 = ttt.winner(self.board_4)
        self.assertEqual(winner_4, X)

        winner_5 = ttt.winner(self.board_5)
        self.assertEqual(winner_5, O)

        winner_6 = ttt.winner(self.board_6)
        self.assertEqual(winner_6, X)

        winner_7 = ttt.winner(self.board_7)
        self.assertEqual(winner_7, O)

    def test_utility(self):

        utility_4 = ttt.utility(self.board_4)
        self.assertEqual(utility_4, 1)

        utility_5 = ttt.utility(self.board_5)
        self.assertEqual(utility_5, -1)

        utility_6 = ttt.utility(self.board_6)
        self.assertEqual(utility_6, 1)

    def test_terminal(self):

        terminal_7 = ttt.terminal(self.board_7)
        self.assertEqual(terminal_7, True)

    def test_winner(self):
        winner_1 = ttt.winner(self.board_1)
        self.assertEqual(winner_1, None)

        winner_2 = ttt.winner(self.board_2)
        self.assertEqual(winner_2, None)

        winner_3 = ttt.winner(self.board_3)
        self.assertEqual(winner_3, None)

        winner_4 = ttt.winner(self.board_4)
        self.assertEqual(winner_4, X)

        winner_5 = ttt.winner(self.board_5)
        self.assertEqual(winner_5, O)

        winner_6 = ttt.winner(self.board_6)
        self.assertEqual(winner_6, X)

        winner_7 = ttt.winner(self.board_7)
        self.assertEqual(winner_7, O)


if __name__ == '__main__':
    unittest.main()
