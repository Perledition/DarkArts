# this file includes all kind of spells
import pygame
from global_utilites.utilits import define_rect, in_rect
from settings.global_constants import window_heigth, window_width


class SpellBase(object):

    def __init__(self, x, y, radius, color, facing, owner):
        self.x = x
        self.y = y
        self.x_vel = self.x
        self.y_vel = self.y
        self.target = (self.x, self.y)
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 5 * facing
        self.owner = owner
        self.damage_dealt = False
        self.dx, self.dy = 0, 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def get_direct_indicators(self):
        """
        This function creates to parameters which will be indicators for the direction of the movement.
        Therefore a parameter will be 1 or -1. 1 indicates a movement in the positive direction, while -1 stands
        for the negative case. This is calculated for the x and y coordinate.

        :return: (tuple): with two values (x, y). Both will be default 1. But can have 1 or -1 as explained above
        """

        # create a pair of x and y values: e.g[(x start, x goal), (y start, y goal)]
        coordinate_pairs = list(zip([self.x, self.y], list(self.target)))

        # set return values with default value
        xd, yd = 1, 1

        # loop through both pairs of coordinates
        for coordinate in coordinate_pairs:

            # get index of coordinate pairs to decide if x or y axis is relevant
            ix = coordinate_pairs.index(coordinate)

            # check if distance between points is not zero and if x or y has to be updated
            if ((coordinate[1] - coordinate[0]) != 0) and (ix == 0):

                # calculate the distance and devide by the abs of distance to get 1 with the positive or negative sign
                xd = (self.target[0] - self.x)/abs((self.target[0] - self.x))

            # same as above but just for y
            if ((coordinate[1] - coordinate[0]) != 0) and (ix == 1):
                yd = (self.target[1] - self.y)/abs((self.target[1] - self.y))

        return xd, yd

    def update(self, damage_indicator):
        self.damage_dealt = damage_indicator

        # update the spell position
        if not self.damage_dealt or in_rect((self.x, self.y), (0, 0, window_width, window_heigth)):
            self.x += self.dx * self.x_vel
            self.y += self.dy * self.y_vel


class Stupor(SpellBase):

    def __init__(self, x, y, radius, color, facing, owner):
        super().__init__(x, y, radius, color, facing, owner)
        self.damage = 3
        self.magic_cost = 20
        self.cool_down = 5





