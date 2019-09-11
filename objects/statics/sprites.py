# standard module import
import os

# third party module import
import pygame

# project module import
from settings.global_constants import ROOT_PATH

# TODO: create automatic path selection

# defines lists of images for the walking animation
SKIN_PATH = os.path.join(ROOT_PATH, 'objects/statics/player/standings/standings')

# lists of sprites for each direction
up = [pygame.image.load(os.path.join(SKIN_PATH, '1.png'))]
up_right = [pygame.image.load(os.path.join(SKIN_PATH, '2.png'))]
right = [pygame.image.load(os.path.join(SKIN_PATH, '3.png'))]
down_right = [pygame.image.load(os.path.join(SKIN_PATH, '4.png'))]
down = [pygame.image.load(os.path.join(SKIN_PATH, '5.png'))]
down_left = [pygame.image.load(os.path.join(SKIN_PATH, '6.png'))]
left = [pygame.image.load(os.path.join(SKIN_PATH, '7.png'))]
up_left = [pygame.image.load(os.path.join(SKIN_PATH, '8.png'))]

char = [up, up_right, right, down_right, down, down_left, left, up_left]

# define static images needed in the functions
arena = pygame.image.load(os.path.join('/Users/maximperl/PycharmProjects/Privat/DarkArts/menus/images/level', 'level.png'))