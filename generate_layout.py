from random import randint
from copy import deepcopy


def new_layout(board_width: int, board_height, mine_count: int) -> list[list[tuple[int, list[tuple[int, int]]]]]:
    # generate base board
    row = [0] * board_width
    gameboard = []
    for i in range(board_height):
        gameboard.append(deepcopy(row))

    # this is an empty copy of the gameboard that will be used to store output board
    out_board = deepcopy(gameboard)

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

            if x == 0 and y == 0:  # top left corner
                surroundings = [(0, 1), (1, 0), (1, 1)]
            elif x == 0 and 0 < y < height:  # left edge
                surroundings = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, 1)]
            elif x == 0 and y == height:  # bottom left corner
                surroundings = [(-1, 0), (-1, 1), (0, 1)]
            elif 0 < x < width and y == height:  # bottom edge
                surroundings = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1)]
            elif x == width and y == height:  # bottom right corner
                surroundings = [(-1, -1), (-1, 0), (0, -1)]
            elif x == width and 0 < y < height:  # right edge
                surroundings = [(-1, -1), (-1, 0), (0, -1), (1, -1), (1, 0)]
            elif x == width and y == 0:  # top right corner
                surroundings = [(0, -1), (1, -1), (1, 0)]
            elif 0 < x < width and y == 0:  # top edge
                surroundings = [(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            else:
                surroundings = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            surrounding_cells: list[tuple[int, int]] = [(y + offy, x + offx) for offy, offx in surroundings]
            surrounded_mines = sum([gameboard[checkY][checkX] == 9 for checkY, checkX in surrounding_cells])

            out_board[y][x] = (surrounded_mines, surrounding_cells)
    return out_board
