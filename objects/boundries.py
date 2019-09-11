# this file holds all boundry elements e.g. walls

# standard module imports

# third party module imports
import pygame

# project module imports
from settings.global_constants import TILE_SIZE


class Wall:

    def __init__(self, x, y):
        self.rect = (x, y, TILE_SIZE, TILE_SIZE)
        self.color = (0, 255, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
