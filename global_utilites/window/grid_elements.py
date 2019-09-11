# grid specific functions for the game

# standard module imports


# third party module imports
import pygame

# project module imports
from settings.global_constants import GAME_HEIGTH, GAME_WIDTH, TILE_SIZE


def draw_grid(screen):
    for x in range(0, GAME_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (165, 165, 165), (x, 0), (x, GAME_HEIGTH))
    for y in range(0, GAME_HEIGTH, TILE_SIZE):
        pygame.draw.line(screen, (165, 165, 165),  (0, y), (GAME_WIDTH, y))
