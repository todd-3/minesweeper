import pygame.mouse
from pygame.sprite import Sprite
from pygame.surface import Surface


class Pointer(Sprite):
    def __init__(
            self,
            shovel_art: Surface,
            flag_art: Surface,
            size: tuple[int, int]
    ) -> None:
        Sprite.__init__(self)
        self.main = shovel_art
        self.secondary = flag_art
        self.rect = self.main.get_rect()

        self.state = True

    def update_state(self) -> bool:
        self.state = not self.state
        return self.state

    def update(self) -> None:
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        if self.state: self.image = self.main
        else:           self.image = self.secondary
