import pygame
from generate_layout import new_layout
from sprites import Pointer

BOARD_SIZE = 15, 15
MINE_COUNT = 30
screen_size = (500, 600)

if __name__ == "__main__":
    board_layout = new_layout(*BOARD_SIZE, MINE_COUNT)  # lay new mines
    print(*[' '.join([str(item) for item in row]) for row in board_layout], sep='\n')  # Prints board list - I know it's a mess

    # set up window
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("MINESWEEPER")
    pygame.display.set_icon(pygame.image.load("assets/window_icon.png").convert())
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    cell_size = (30, 30)
    flag_size = (20, 20)

    # load art
    primary_cell_art = ["cell_0.png", "cell_1.png", "cell_2.png", "cell_3.png", "cell_4.png", "cell_5.png", "cell_6.png", "cell_7.png", "cell_8.png", "cell_mine.png"]
    cell_assets = [pygame.image.load("assets/" + file).convert() for file in primary_cell_art]
    flag = pygame.image.load("assets/flag.png")
    shovel = pygame.image.load("assets/shovel.png")
    cover_cell = pygame.image.load("assets/cell_covered.png")

    # build rest of assets
    flagged_cell = pygame.image.load("assets/cell_covered.png")
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

        # display field
        screen.fill("white")

        base_rec = pygame.Rect(25, 125, *cell_size)
        for y, row in enumerate(board_layout):
            for x, cell_info in enumerate(row):
                screen.blit(flagged_cell, base_rec.move(x * cell_size[0], y * cell_size[1]))

        pointer_group.update()
        pointer_group.draw(screen)

        pygame.display.flip()

    pygame.quit()
