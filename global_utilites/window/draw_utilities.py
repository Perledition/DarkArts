# this file includes everything needed for the camera movement and global map settings

# standard module imports

# third party module imports
import pygame

# project module imports


class Map:

    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * TILE_SIZE
        self.height = self.tile_height * TILE_SIZE


class Camera:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

