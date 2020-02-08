"""
Tic Tac Toe Player
"""

import math
from random import randint
from copy import deepcopy
from helper import count_value, get_positions_of_value, get_winning_position_sets, minimax_run

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = count_value(board, X)
    o_count = count_value(board, O)
    if x_count == 0:
        player = X
    elif x_count > o_count:
        player = O
    else:
        player = X
    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
    else:
        empty_positions = get_positions_of_value(board, EMPTY)
        return empty_positions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    empty_positions = get_positions_of_value(board, EMPTY)
    if action not in empty_positions:
        print('Illegal action: ', action)
        raise ValueError('This move is illegal.')
    # Make deep copy of board to prevent direct mutation
    board_copy = deepcopy(board)
    current_player = player(board_copy)
    row, col = action
    board_copy[row][col] = current_player
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    player = None
    # Get positions of two players
    x_positions = get_positions_of_value(board, X)
    o_positions = get_positions_of_value(board, O)
    # Get all sets of winning positions
    winning_positions = get_winning_position_sets()
    # Compare them
    for win_set in winning_positions:
        if win_set.issubset(x_positions):
            player = X
            break
        elif win_set.issubset(o_positions):
            player = O
            break
    return player

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If no empty spaces
    empty_positions = get_positions_of_value(board, EMPTY)
    if not empty_positions:
        game_over = True
    elif utility(board) in [-1, 1]:
        game_over = True
    else:
        game_over = False

    return game_over


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    if player == X:
        game_value = 1
    elif player == O:
        game_value = -1
    else:
        game_value = 0
    return game_value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        best_action = None
        cur_player = player(board)
        empty_positions = get_positions_of_value(board, EMPTY)
        if cur_player == X:
            best_score = float("-inf")
            for pos in empty_positions:
                board_result = result(board, pos)
                score = get_best_score(board_result)
                if (score > best_score):
                    best_score = score
                    best_action = pos
            # return best_action
        elif cur_player == O:
            best_action = None
            best_score = float("inf")
            for pos in empty_positions:
                board_result = result(board, pos)
                score = get_best_score(board_result)
                if (score < best_score):
                    best_score = score
                    best_action = pos
            # return best_action
        else:
            raise ValueError('Player must be X or O.')
    return best_action

def get_best_score(board):
    if terminal(board):
        return utility(board)
    else:
        cur_player = player(board)
        empty_positions = get_positions_of_value(board, EMPTY)
        if cur_player == X:
            best_score = float("-inf")
            for pos in empty_positions:
                board_result = result(board, pos)
                score = get_best_score(board_result)
                best_score = max(best_score, score)
            return best_score
        elif cur_player == O:
            best_score = float("inf")
            for pos in empty_positions:
                board_result = result(board, pos)
                score = get_best_score(board_result)
                best_score = min(best_score, score)
            return best_score
        else:
            raise ValueError('Player must be X or O.')
