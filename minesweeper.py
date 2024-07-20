import pygame
from generate_layout import new_layout
from sprites import Pointer
from random import seed
from math import floor


seed(10)
BOARD_SIZE = 15, 15
MINE_COUNT = 30

def explore_zeros(field: list, cor: tuple[int, int]):
    for spos in field[cor[0]][cor[1]][2]:
        if field[spos[0]][spos[1]][0] == 0 and field[spos[0]][spos[1]][1] != 2:
            field[spos[0]][spos[1]][1] = 2
            explore_zeros(field, spos)
        else: field[spos[0]][spos[1]][1] = 2

if __name__ == "__main__":

    cell_size = (30, 30)
    flag_size = (20, 20)
    display_offset = (25, 125)
    screen_size = (BOARD_SIZE[0] * cell_size[0] + display_offset[0] * 2, display_offset[0] + display_offset[1] + BOARD_SIZE[1] * cell_size[1])

    board_boundaries = (
        (display_offset[0], screen_size[0] - display_offset[0]),
        (display_offset[1], screen_size[1] - display_offset[0])
    )
    print("Window Size: %ix%i" % (screen_size[0], screen_size[1]))

    # lay new mines
    # returned board is of a format:
    #  row (y)
    #    column (x)
    #      cell:
    #        surrounding mine count
    #        state tracker (0: covered, 1: flagged, 2: uncovered)
    #        surrounding cell coordinates
    board_layout: list[list[list[int, int, list[tuple[int, int]]]]] = new_layout(*BOARD_SIZE, MINE_COUNT)
    print(*[' '.join([str(item[0]) for item in row]) for row in board_layout], sep='\n')  # Prints board list - I know it's a mess

    # set up window
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("MINESWEEPER")
    pygame.display.set_icon(pygame.image.load("assets/window_icon.png").convert())
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # load art
    # TODO - figure out how to .convert() flag and shovel while retaining transparency
    primary_cell_art = ["cell_0.png", "cell_1.png", "cell_2.png", "cell_3.png", "cell_4.png", "cell_5.png", "cell_6.png", "cell_7.png", "cell_8.png", "cell_mine.png"]
    cell_assets = [pygame.image.load("assets/" + file).convert() for file in primary_cell_art]
    flag = pygame.image.load("assets/flag.png")
    shovel = pygame.image.load("assets/shovel.png")
    cover_cell = pygame.image.load("assets/cell_covered.png").convert()

    # build rest of assets
    flagged_cell = pygame.image.load("assets/cell_covered.png").convert()
    flagged_cell.blit(flag, pygame.Rect(6, 6, *flag_size))

    # set pointer class
    cursor = Pointer(
        shovel_art=shovel,
        flag_art=flag,
        size=(20, 20)
    )
    pointer_group = pygame.sprite.GroupSingle(cursor)

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cursor.update_state()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # make sure click was within game board
                if (board_boundaries[0][0] < pos[0] < board_boundaries[0][1]
                        and board_boundaries[1][0] < pos[1] < board_boundaries[1][1]):
                    # determine which cell was clicked
                    click_x = floor((pos[0] - display_offset[0]) / cell_size[0])
                    click_y = floor((pos[1] - display_offset[1]) / cell_size[1])

                    if board_layout[click_y][click_x][1] == 2:  # if cell is already uncovered
                        # get a list of all unflagged surrounding cells
                        unflagged = [(check_y, check_x) for check_y, check_x in board_layout[click_y][click_x][2] if board_layout[check_y][check_x][1] != 1]
                        surrounding_flagged = len(board_layout[click_y][click_x][2]) - len(unflagged)

                        if board_layout[click_y][click_x][0] == surrounding_flagged:
                            for check_y, check_x in unflagged:
                                if board_layout[click_y][click_x][0] == 0:
                                    board_layout[check_y][check_x][1] = 2
                                    explore_zeros(board_layout, (click_y, click_x))
                                else: board_layout[check_y][check_x][1] = 2
                        elif board_layout[click_y][click_x][0] == 9:  # you clicked a mine!!
                            running = False
                            print("------ GAME OVER! ------")

                    elif cursor.state:  # cursor is in shovel mode
                        board_layout[click_y][click_x][1] = 2
                        if board_layout[click_y][click_x][0] == 9:  # you clicked a mine!!
                            running = False
                        elif board_layout[click_y][click_x][0] == 0:
                            explore_zeros(board_layout, (click_y, click_x))
                    elif board_layout[click_y][click_x][1] == 1:  # can assume flag mode
                        board_layout[click_y][click_x][1] = 0  # if already flagged, reset to normal covered
                    else:  # flag cell
                        board_layout[click_y][click_x][1] = 1

        # display field
        screen.fill("white")

        base_rec = pygame.Rect(*display_offset, *cell_size)
        for y, row in enumerate(board_layout):
            for x, cell_info in enumerate(row):
                if cell_info[1] == 0:
                    art = cover_cell
                elif cell_info[1] == 1:
                    art = flagged_cell
                else:
                    art = cell_assets[cell_info[0]]
                screen.blit(art, base_rec.move(x * cell_size[0], y * cell_size[1]))

        pointer_group.update()
        pointer_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
