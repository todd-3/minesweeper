import pygame
from generate_layout import new_layout
from sprites import Pointer
from random import seed
from math import floor
import assets


seed(10)
BOARD_SIZE = 15, 15
MINE_COUNT = 30
CELL_SIZE = (30, 30)
FLAG_SIZE = (20, 20)
COUNTER_SIZE = (45, 80)
PADDING = 25


def explore_zeros(field: list, cor: tuple[int, int]):
    for spos in field[cor[0]][cor[1]][2]:
        if field[spos[0]][spos[1]][1] == 1: continue  # if a cell is flagged, don't show it
        elif field[spos[0]][spos[1]][0] == 0 and field[spos[0]][spos[1]][1] != 2:
            field[spos[0]][spos[1]][1] = 2
            explore_zeros(field, spos)
        else: field[spos[0]][spos[1]][1] = 2


if __name__ == "__main__":

    screen_size = (
        BOARD_SIZE[0] * CELL_SIZE[0] + PADDING * 2,
        BOARD_SIZE[1] * CELL_SIZE[1] + PADDING * 3 + COUNTER_SIZE[1]
    )
    bounds = (  # the pixel bounds of the minefield on screen
        (PADDING, screen_size[0] - PADDING),
        (PADDING * 2 + COUNTER_SIZE[1], screen_size[1] - PADDING)
    )
    print("Window Size: %ix%i" % (screen_size[0], screen_size[1]))

    score_places = len(str(MINE_COUNT))  # number of 7-segment entities that will be needed to count score
    score_offset = floor((screen_size[0] - COUNTER_SIZE[0] * score_places) / 2)  # left edge of left-most scoring segment
    # score_placement = [  # (x, y) position of each score segment
    #     (score_offset + COUNTER_SIZE[0] * i, PADDING) for i in range(score_places)
    # ]

    top_left_corner = (PADDING, PADDING * 2 + COUNTER_SIZE[1])

    # lay new mines
    # returned board is of a format:
    #  row (y)
    #    column (x)
    #      cell:
    #        surrounding mine count
    #        state tracker (0: covered, 1: flagged, 2: uncovered)
    #        surrounding cell coordinates (list)
    board_layout: list[list[list[int, int, list[tuple[int, int]]]]] = new_layout(*BOARD_SIZE, MINE_COUNT)
    print(*[' '.join([str(item[0]) for item in row]) for row in board_layout], sep='\n')  # Prints board list - I know it's a mess

    # set up window
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("MINESWEEPER")
    pygame.display.set_icon(pygame.image.load(assets.assets[2]).convert())
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # load art
    # TODO - figure out how to .convert() flag and shovel while retaining transparency
    cell_assets = [pygame.image.load(file).convert() for file in assets.cells]
    score_segments = [pygame.image.load(file).convert() for file in assets.score_display]
    flag = pygame.image.load(assets.assets[0])
    shovel = pygame.image.load(assets.assets[1])

    cell_assets.append(pygame.image.load(assets.cells[10]).convert())  # duplicate covered cell into art list
    cell_assets[11].blit(flag, pygame.Rect(6, 6, *FLAG_SIZE))  # blit flag onto duplicated cover

    # set pointer class
    cursor = Pointer(
        shovel_art=shovel,
        flag_art=flag,
        size=FLAG_SIZE
    )
    pointer_group = pygame.sprite.GroupSingle(cursor)

    running = True
    game_state = 0

    # if flags_placed + cells_opened = board_size * board_height, game is won
    flags_placed = 0
    total_cells = BOARD_SIZE[0] * BOARD_SIZE[1]

    while running and not game_state:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: cursor.update_state()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # player clicked
                pos = pygame.mouse.get_pos()

                # make sure click was within game board
                if bounds[0][0] < pos[0] < bounds[0][1] and bounds[1][0] < pos[1] < bounds[1][1]:
                    # determine which cell was clicked
                    click_x = floor((pos[0] - PADDING) / CELL_SIZE[0])
                    click_y = floor((pos[1] - top_left_corner[1]) / CELL_SIZE[1])
                    clicked_cell = board_layout[click_y][click_x]

                    if board_layout[click_y][click_x][1] == 2:  # if cell is already uncovered
                        # get a list of all unflagged surrounding cells
                        unflagged = [(check_y, check_x) for check_y, check_x in clicked_cell[2] if board_layout[check_y][check_x][1] != 1]
                        surrounding_flagged = len(board_layout[click_y][click_x][2]) - len(unflagged)

                        # check if the number of surrounding cells flag is equivalent to the cell's mine count
                        # if it is, uncover all unflagged surrounding cells
                        if clicked_cell[0] == surrounding_flagged:
                            for check_y, check_x in unflagged:
                                if clicked_cell[0] == 0:
                                    board_layout[check_y][check_x][1] = 2
                                    explore_zeros(board_layout, (click_y, click_x))
                                else: board_layout[check_y][check_x][1] = 2
                        elif clicked_cell[0] == 9: game_state = 1  # you clicked a mine!!

                    elif cursor.state:  # cursor is in shovel mode
                        clicked_cell[1] = 2
                        if clicked_cell[0] == 9: game_state = 1  # you clicked a mine!!
                        elif clicked_cell[0] == 0: explore_zeros(board_layout, (click_y, click_x))  # if empty cell, expose all other surrounding 0s

                    # can assume the cursor is in flag mode beyond this point
                    elif clicked_cell[1] == 1:  # if already flagged, reset to normal covered
                        clicked_cell[1] = 0
                        flags_placed -= 1
                    else:  # flag cell
                        clicked_cell[1] = 1
                        flags_placed += 1

        # display field
        screen.fill("white")

        score_rec = pygame.Rect(score_offset, PADDING, *COUNTER_SIZE)
        segment_numbers = [int(i) for i in str(flags_placed).zfill(score_places)]
        for i in range(score_places):
            screen.blit(score_segments[segment_numbers[i]], score_rec.move(COUNTER_SIZE[0] * i, 0))

        cells_opened = 0
        base_rec = pygame.Rect(*top_left_corner, *CELL_SIZE)
        for y, row in enumerate(board_layout):
            for x, cell_info in enumerate(row):
                if cell_info[1] == 0:
                    art = cell_assets[10]
                elif cell_info[1] == 1:
                    art = cell_assets[11]
                else:
                    art = cell_assets[cell_info[0]]
                    cells_opened += 1
                screen.blit(art, base_rec.move(x * CELL_SIZE[0], y * CELL_SIZE[1]))

        if flags_placed == MINE_COUNT and cells_opened + flags_placed == total_cells: game_state = 2  # you won!

        pointer_group.update()
        pointer_group.draw(screen)

        pygame.display.flip()

    if running:
        if game_state == 1:
            print("You hit a mine!\n------ GAME OVER! ------")
        if game_state == 2:
            print("You win!")

    pygame.quit()
