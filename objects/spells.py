# this file includes all kind of spells
import pygame


class SpellBase(object):

    def __init__(self, x, y, radius, color, facing, owner):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        self.owner = owner

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def update(self):
        # update the spell position
        self.x += self.vel
        self.y += self.vel


class Stupor(SpellBase):

    def __init__(self, x, y, radius, color, facing, owner):
        super().__init__(x, y, radius, color, facing, owner)
        self.damage = 3
        self.magic_cost = 20
        self.cool_down = 2





