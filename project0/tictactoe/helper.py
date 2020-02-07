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
