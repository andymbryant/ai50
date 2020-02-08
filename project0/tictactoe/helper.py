X = "X"
O = "O"
EMPTY = None

def count_value(board, value):
    count = 0
    for row in board:
        for cell in row:
            if cell == value:
                count += 1
    return count

def get_positions_of_value(board, value):
    positions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == value:
                position = (i, j)
                positions.add(position)
    return positions

def get_winning_position_sets():
    return (
        # Full rows
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},
        # Full columns
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},
        # Diagonal
        {(0, 0), (1, 1), (2, 2)},
        # Alt-diagonal
        {(0, 2), (1, 1), (2, 0)}
    )


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

def minimax_run(board):
    cur_player = player(board)
    empty_positions = get_positions_of_value(board, EMPTY)
    if cur_player == X:
        opt_action = None
        max_score = -math.inf
        for pos in empty_positions:
            board_result = result(board, pos)
            opt_action, opt_score = minimax_run(board_result)
            if (opt_score > max_score):
                max_score = opt_score
                opt_action = pos
    elif cur_player == O:
        opt_action = None
        min_score = math.inf
        for pos in empty_positions:
            board_result = result(board, pos)
            opt_action, opt_score = minimax(board_result)
            if (opt_score < min_score):
                min_score = opt_score
                opt_action = pos
    else:
        raise ValueError('Player must be X or O.')
    return (opt_action, opt_score)
