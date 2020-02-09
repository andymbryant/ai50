"""
Tic Tac Toe Player
"""

import math
from random import randint
from copy import deepcopy
from helper import count_value, get_positions_of_value, get_winning_position_sets

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
    # Get nunber of X's and O's
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
        raise ValueError('This move is illegal.')

    # Make deep copy of board to prevent direct mutation
    board_copy = deepcopy(board)
    current_player = player(board_copy)
    row, col = action
    # Take the action on the copy of the board
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
    # Compare them with positions occupied by each player
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
    empty_positions = get_positions_of_value(board, EMPTY)
    # If the board is full, the game is over
    if not empty_positions:
        game_over = True
    # If either player has won, the game is over
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
        current_player = player(board)
        empty_positions = get_positions_of_value(board, EMPTY)
        if current_player == X:
            # Initialize best score with lowest possible number
            best_score = float("-inf")
            # Check each available move on the board
            for pos in empty_positions:
                board_result = result(board, pos)
                # Get result of that move
                score = get_best_score(board_result)
                # Check against existing best score
                # X player wants a higher score
                if (score > best_score):
                    best_score = score
                    best_action = pos
                # Naive pruning
                if best_score == 1:
                    break
            return best_action
        elif current_player == O:
            best_action = None
            # Initialize best score with highest possible number
            best_score = float("inf")
            # Check each available move on the board
            for pos in empty_positions:
                board_result = result(board, pos)
                # Get result of that move
                score = get_best_score(board_result)
                # Check against existing best score
                # O player wants a lower score
                if (score < best_score):
                    best_score = score
                    best_action = pos
                # Naive pruning
                if best_score == -1:
                    break
            return best_action
        else:
            raise ValueError('Player must be X or O.')

def get_best_score(board):
    """
    Recursive helper function for minimax that returns the best score by player
    """
    # Base case, return the result of the board
    if terminal(board):
        return utility(board)
    else:
        current_player = player(board)
        empty_positions = get_positions_of_value(board, EMPTY)
        if current_player == X:
            # Initialize best score with lowest possible number
            best_score = float("-inf")
            # Check each available move on the board
            for pos in empty_positions:
                board_result = result(board, pos)
                # Get result of that move
                score = get_best_score(board_result)
                # Check against existing best score and get max for X player
                best_score = max(best_score, score)
            return best_score
        elif current_player == O:
            # Initialize best score with highest possible number
            best_score = float("inf")
            # Check each available move on the board
            for pos in empty_positions:
                board_result = result(board, pos)
                # Get result of that move
                score = get_best_score(board_result)
                # Check against existing best score and get min for O player
                best_score = min(best_score, score)
            return best_score
        else:
            raise ValueError('Player must be X or O.')
