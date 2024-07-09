# generate a gameboard of size x by y and populate randomly with "mines"
from random import randint
from copy import deepcopy

BOARD_WIDTH = 15
BOARD_HEIGHT = 15
MINE_COUNT = 40

# generate board
row = [0] * BOARD_WIDTH
gameboard = []
for i in range(BOARD_HEIGHT):
    gameboard.append(deepcopy(row))

# generated gameboard is accessed using board[y][x]

# populate with mines
counter = MINE_COUNT
while counter > 0:
    x_pos, y_pos = randint(0, BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1)
    if gameboard[y_pos][x_pos]:
        pass
    else:
        gameboard[y_pos][x_pos] = 9
        counter -= 1

# calculates mine surround count for each position
width = BOARD_WIDTH - 1  # offset board width and height by one to account for lists being 0 indexed
height = BOARD_HEIGHT - 1
for y, row in enumerate(gameboard):
    for x, cell in enumerate(row):
        if cell == 9:  # don't check if cell is a mine
            continue

        mine_count = 0
        if x == 0 and y == 0:  # top left corner
            mine_count += gameboard[y][x + 1] == 9
            mine_count += gameboard[y + 1][x] == 9
            mine_count += gameboard[y + 1][x + 1] == 9
        elif x == 0 and 0 < y < height:  # left edge
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y - 1][x + 1] == 9
            mine_count += gameboard[y][x + 1] == 9
            mine_count += gameboard[y + 1][x] == 9
            mine_count += gameboard[y + 1][x + 1] == 9
        elif x == 0 and y == height:  # bottom left corner
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y - 1][x + 1] == 9
            mine_count += gameboard[y][x + 1] == 9
        elif 0 < x < width and y == height:  # bottom edge
            mine_count += gameboard[y - 1][x - 1] == 9
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y - 1][x + 1] == 9
            mine_count += gameboard[y][x - 1] == 9
            mine_count += gameboard[y][x + 1] == 9
        elif x == width and y == height:  # bottom right corner
            mine_count += gameboard[y - 1][x - 1] == 9
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y][x - 1] == 9
        elif x == width and 0 < y < height:  # right edge
            mine_count += gameboard[y - 1][x - 1] == 9
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y][x - 1] == 9
            mine_count += gameboard[y + 1][x - 1] == 9
            mine_count += gameboard[y + 1][x] == 9
        elif x == width and y == 0:  # top right corner
            mine_count += gameboard[y][x - 1] == 9
            mine_count += gameboard[y + 1][x - 1] == 9
            mine_count += gameboard[y + 1][x] == 9
        elif 0 < x < width and y == 0:  # top edge
            mine_count += gameboard[y][x - 1] == 9
            mine_count += gameboard[y][x + 1] == 9
            mine_count += gameboard[y + 1][x - 1] == 9
            mine_count += gameboard[y + 1][x] == 9
            mine_count += gameboard[y + 1][x + 1] == 9
        else:
            mine_count += gameboard[y - 1][x - 1] == 9
            mine_count += gameboard[y - 1][x] == 9
            mine_count += gameboard[y - 1][x + 1] == 9
            mine_count += gameboard[y][x - 1] == 9
            mine_count += gameboard[y][x + 1] == 9
            mine_count += gameboard[y + 1][x - 1] == 9
            mine_count += gameboard[y + 1][x] == 9
            mine_count += gameboard[y + 1][x + 1] == 9

        gameboard[y][x] = mine_count


print(*[' '.join([str(item) for item in row]) for row in gameboard], sep='\n')  # Prints board - I know it's a mess
