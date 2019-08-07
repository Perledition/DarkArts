# this file includes all kind of spells
import pygame


class Stupor(object):

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
