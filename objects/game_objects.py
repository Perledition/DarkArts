# find all the Game objects in here
import pygame
from .spells import *
from settings.global_constants import window_heigth, window_width


class Player:

    def __init__(self, x, y, width, height, color):
        self.x = x  # defines position on x-axis
        self.y = y  # defines position on y-axis
        self.width = width
        self.height = height
        self.color = color  # defines the color of the player rectangle
        self.rect = (x, y, width, height)  # defines the rectangle as player object defined height*width
        self.vel = 3    # defines the speed of the object when pressing key
        self.standing = True
        self.spells = []

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        # update the player position
        self.rect = (self.x, self.y, self.width, self.height)

    def move(self):

        # returns a list of keys and if they are pressed the value will be a one
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < window_width - self.width - self.vel:
            self.x += self.vel

        if keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < window_heigth - self.vel:
            self.y += self.vel

        if keys[pygame.K_a]:
            self.spells.append((Stupor(round(self.x + self.width//2), round(self.y + self.height//2), 6, (104, 44, 0), self.vel)))

        self.update()






