import pygame
from generate_layout import new_layout

BOARD_SIZE = 15, 15
MINE_COUNT = 30
screen_size = (500, 600)

ART = ["cell_0.png", "cell_1.png", "cell_2.png", "cell_3.png", "cell_4.png", "cell_5.png", "cell_6.png", "cell_7.png", "cell_8.png", "cell_mine.png"]
ART_SIZE = (30, 30)

if __name__ == "__main__":
    board_layout = new_layout(*BOARD_SIZE, MINE_COUNT)  # lay new mines
    print(*[' '.join([str(item) for item in row]) for row in board_layout], sep='\n')  # Prints board list - I know it's a mess

    # set up window
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("MINESWEEPER")
    pygame.display.set_icon(pygame.image.load("assets/window_icon.png").convert())
    clock = pygame.time.Clock()

    # load cell art
    cell_assets = [pygame.image.load("assets/" + file).convert() for file in ART]

    # display field
    screen.fill("white")

    base_rec = pygame.Rect(25, 125, *ART_SIZE)
    for y, row in enumerate(board_layout):
        for x, cell_info in enumerate(row):
            screen.blit(cell_assets[cell_info], base_rec.move(x * ART_SIZE[0], y * ART_SIZE[1]))

    pygame.display.flip()

    running = True
    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
