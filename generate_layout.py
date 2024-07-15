from random import randint
from copy import deepcopy


def new_layout(board_width: int, board_height, mine_count: int) -> list[list[int]]:
    # generate base board
    row = [0] * board_width
    gameboard = []
    for i in range(board_height):
        gameboard.append(deepcopy(row))

    # this is an empty copy of the gameboard that will be used to store additional state information
    # gameboard_mask = deepcopy(gameboard)

    # gameboard is accessed using board[y][x]

    # populate with mines
    counter = mine_count
    while counter > 0:
        x_pos, y_pos = randint(0, board_width - 1), randint(0, board_height - 1)
        if gameboard[y_pos][x_pos]:
            pass
        else:
            gameboard[y_pos][x_pos] = 9
            counter -= 1

    # calculates mine surround count for each position
    width = board_width - 1  # offset board width and height by one to account for lists being 0 indexed
    height = board_height - 1
    for y, row in enumerate(gameboard):
        for x, cell in enumerate(row):
            if cell == 9:  # don't check if cell is a mine
                continue

            surrounded_count = 0
            if x == 0 and y == 0:  # top left corner
                surrounded_count += gameboard[y][x + 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
                surrounded_count += gameboard[y + 1][x + 1] == 9
            elif x == 0 and 0 < y < height:  # left edge
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y - 1][x + 1] == 9
                surrounded_count += gameboard[y][x + 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
                surrounded_count += gameboard[y + 1][x + 1] == 9
            elif x == 0 and y == height:  # bottom left corner
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y - 1][x + 1] == 9
                surrounded_count += gameboard[y][x + 1] == 9
            elif 0 < x < width and y == height:  # bottom edge
                surrounded_count += gameboard[y - 1][x - 1] == 9
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y - 1][x + 1] == 9
                surrounded_count += gameboard[y][x - 1] == 9
                surrounded_count += gameboard[y][x + 1] == 9
            elif x == width and y == height:  # bottom right corner
                surrounded_count += gameboard[y - 1][x - 1] == 9
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y][x - 1] == 9
            elif x == width and 0 < y < height:  # right edge
                surrounded_count += gameboard[y - 1][x - 1] == 9
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y][x - 1] == 9
                surrounded_count += gameboard[y + 1][x - 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
            elif x == width and y == 0:  # top right corner
                surrounded_count += gameboard[y][x - 1] == 9
                surrounded_count += gameboard[y + 1][x - 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
            elif 0 < x < width and y == 0:  # top edge
                surrounded_count += gameboard[y][x - 1] == 9
                surrounded_count += gameboard[y][x + 1] == 9
                surrounded_count += gameboard[y + 1][x - 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
                surrounded_count += gameboard[y + 1][x + 1] == 9
            else:
                surrounded_count += gameboard[y - 1][x - 1] == 9
                surrounded_count += gameboard[y - 1][x] == 9
                surrounded_count += gameboard[y - 1][x + 1] == 9
                surrounded_count += gameboard[y][x - 1] == 9
                surrounded_count += gameboard[y][x + 1] == 9
                surrounded_count += gameboard[y + 1][x - 1] == 9
                surrounded_count += gameboard[y + 1][x] == 9
                surrounded_count += gameboard[y + 1][x + 1] == 9

            gameboard[y][x] = surrounded_count
    return gameboard
