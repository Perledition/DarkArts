# find all the Game objects in here
import os
from .spells import *
from settings.global_constants import window_heigth, window_width


class Player:

    def __init__(self, x, y, width, height, color, attributes, player_id):
        self.id = player_id
        self.x = x  # defines position on x-axis
        self.y = y  # defines position on y-axis
        self.target = (self.x, self.y)  # This is the goal (x, y) coordinate

        self.width = width  # defines the width of the character
        self.height = height  # defines the height of the character
        self.color = color  # defines the color of the player rectangle
        self.rect = (x, y, width, height)  # defines the rectangle as player object defined height*width
        self.speed = 60
        self.x_vel = 0    # defines the speed of the object when pressing key
        self.y_vel = 0  # defines the speed of the object when pressing key
        self.position_map = [False, False, False, False]  # this is a map of boolean values to check the latest position (left, right, top, down)
        self.spells = []  # includes all spells created for the character
        self.walk_count = 0  # keeps track of the steps - needed for the sprites

        # this defines the player conditions

        self.health = attributes[0]
        self.magic = attributes[1]
        self.magic_available = attributes[1]
        self.hitbox = (self.x + 20, self.y + 10, 28, 50)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update_spell(self):
        for spell in self.spells:
            if spell.damage_dealt:
                self.spells.pop(self.spells.index(spell))

            if (spell.x > window_width) or (spell.x < 0) or (spell.y > window_heigth) or (spell.y < 0):
                self.spells.pop(self.spells.index(spell))

    def update(self):
        # update the player position
        self.rect = (self.x, self.y, self.width, self.height)
        if self.walk_count + 1 >= 4:
            self.walk_count = 0

        self.update_spell()

        if self.magic_available < self.magic:
            self.magic_available += 1

    def cast_spell(self, spell_to_cast):
        self.spells.append(spell_to_cast)
        self.magic_available -= spell_to_cast.magic_cost

    def hit(self, damage):
        self.health -= damage
        print('{} damage'.format(damage))
        print('{} health'.format(self.health))

    def move2(self):
        speed = 50/1000
        # this is meant to calculate the direction of the movement
        coordinate_pairs = list(zip([self.x, self.y], list(self.target)))
        xd, yd = 1, 1
        for coordinate in coordinate_pairs:

            # get index of coordinate pairs to decide if x or y axis is relevant
            ix = coordinate_pairs.index(coordinate)

            # check if distance between points is not zero and if x or y has to be updated
            if ((coordinate[1] - coordinate[0]) != 0) and (ix == 0):
                xd = (self.target[0] - self.x)/abs((self.target[0] - self.x))

            if ((coordinate[1] - coordinate[0]) != 0) and (ix == 1):
                yd = (self.target[1] - self.y)/abs((self.target[1] - self.y))

        if (self.target[0] - self.x) != 0 and abs(self.target[0] - self.x) > (self.x_vel*speed):
            self.x += xd * self.x_vel * speed
        else:
            self.x += (self.target[0] - self.x)

        if (self.target[1] - self.y) != 0 and abs(self.target[1] - self.y) > (self.y_vel*speed):
            self.y += yd * self.y_vel * speed
        else:
            self.y += (self.target[1] - self.y)

        self.walk_count += 1

        self.hitbox = (self.x + 20, self.y + 10, 28, 50)
        self.update()

    def move(self):

        # returns a list of keys and if they are pressed the value will be a one
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.position_map[0] = True
            self.position_map[1] = False
            self.walk_count += 1

        if keys[pygame.K_RIGHT] and self.x < window_width - self.width - self.vel:
            self.x += self.vel
            self.position_map[0] = False
            self.position_map[1] = True
            self.walk_count += 1

        if keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel
            self.position_map[2] = True
            self.position_map[3] = False
            self.walk_count = 0

        if keys[pygame.K_DOWN] and self.y < window_heigth - self.vel:
            self.y += self.vel
            self.position_map[2] = False
            self.position_map[3] = True
            self.walk_count = 0

        if keys[pygame.K_a]:
            cast = Stupor(round(self.x + self.width // 2), round(self.y + self.height // 2), 6, (0, 255, 0), 1, self.id)
            if self.magic_available >= cast.magic_cost:
                self.cast_spell(cast)

        self.hitbox = (self.x + 20, self.y + 10, 28, 50)
        self.update()






