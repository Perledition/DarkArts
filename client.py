import pygame
import os
import math
from copy import deepcopy
from network import Network
from settings.global_constants import window_heigth, window_width
from global_utilites.utilits import define_rect, find_angle, define_unique_direction

# TODO: Add Sprites differences for each player - handed over by Object / mayby defined by house at the beginning
# TODO: Load Sprites in different file

# set global window settings
pygame.init()
width = window_width
height = window_heigth
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DarkArena")
# print(pygame.display.list_modes())

# defines lists of images for the walking animation
SKIN_PATH = 'objects/statics/player/standings/standings'

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
arena = pygame.image.load(os.path.join('objects/statics/player/standings/', 'asphalt-883039_1280.jpg'))


def draw_player(plr, window):
    # if we move in the left direction display the image by index of walk_count // same for right
    angle = math.degrees(math.atan2(plr.target[1] - plr.y, plr.target[0] - plr.x)) * (-1)
    plr.direction = define_unique_direction(angle)
    window.blit(char[plr.direction][plr.walk_count], (plr.x, plr.y))

    # draw health bar and bar of magic
    pygame.draw.rect(window, (21, 99, 194), (plr.hitbox[0], plr.hitbox[1] - 100, 50, 5))

    # defines the percentage of what has to be taken down from the players health
    subs_life = (50/plr.start_health) * (plr.start_health - plr.health)
    pygame.draw.rect(window, (19, 161, 3), (plr.hitbox[0], plr.hitbox[1] - 100, 50 - subs_life, 5))

    # do the same but just for the magic
    subs_magic = (50 / plr.magic) * (plr.magic - plr.magic_available)
    pygame.draw.rect(window, (29, 28, 31), (plr.hitbox[0], plr.hitbox[1] - 90, 50, 5))
    pygame.draw.rect(window, (21, 99, 194), (plr.hitbox[0], plr.hitbox[1] - 90, 50 - subs_magic, 5))
    pygame.draw.rect(window, (255, 0, 0), plr.hitbox, 2)


def spell_hit(player, spell, player2):

    # rectangle of player it self
    x1, y1, x2, y2 = define_rect(player.hitbox)

    # rectangle of enemy player
    ex1, ey1, ex2, ey2 = define_rect(player2.hitbox)

    # this function checks if the player it self was hit by an enemy spell
    if (spell.x > x1) and (spell.x < x2) and (spell.y > y1) and (spell.y < y2):
        if spell.owner != player.id:
            player.hit(spell.damage)
            return True

    # this function checks if one of the own spells hits the enemy
    if (spell.x > ex1) and (spell.x < ex2) and (spell.y > ey1) and (spell.y < ey2):
        if spell.owner == player.id:
            player.spells.pop(player.spells.index(spell))


def movement_definitions(target, x, y, speed):
    distance = (target[0] - x, target[1] - y)
    if abs(distance[0]) >= abs(distance[1]):
        x_vel = speed
        y_vel = abs(distance[1]) / (abs(distance[0]) / x_vel)
    else:
        y_vel = speed
        x_vel = abs(distance[0]) / (abs(distance[1]) / y_vel)

    return x_vel, y_vel


# draw the Window which we want to display
def draw_window(window, player, player2):
    win.blit(arena, (0, 0))

    draw_player(player, window)
    draw_player(player2, window)

    # draw all the spells player one has casted
    for sp in player.spells + player2.spells:
        sp.update(spell_hit(player, sp, player2))
        sp.draw(window)

    if player.aim_mode[0]:

        start_pos = (round(player.x + player.width // 2), round(player.y + player.height // 2))

        angle = find_angle(start_pos, pygame.mouse.get_pos())
        line = (round(start_pos[0] + (math.cos(angle) * 150)), round(start_pos[1] - (math.sin(angle) * 150)))

        pygame.draw.line(window, (155, 23, 112), start_pos, line, 10)

    pygame.display.update()


# Defines the main loop which runs until the program gets stopped
def run_game():
    run = True
    n = Network()
    player1 = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        player2 = n.send(player1)

        # update the game window for each event // pygame specific
        for event in pygame.event.get():

            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1) and (not player1.aim_mode[0]):
                player1.target = pygame.mouse.get_pos()
                player1.x_vel, player1.y_vel = movement_definitions(player1.target, player1.x, player1.y, player1.speed)

            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1) and player1.aim_mode[0]:
                spell = deepcopy(player1.spell_collection[player1.aim_mode[1]])
                spell.x = round(player1.x + player1.width // 2)
                spell.y = round(player1.y + player1.height // 2)
                spell.target = pygame.mouse.get_pos()
                spell.x_vel, spell.y_vel = movement_definitions(spell.target, spell.x, spell.y, spell.speed)
                spell.dx, spell.dy = spell.get_direct_indicators()
                player1.cast_spell(spell)
                player1.aim_mode = [False, 0]

            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 3):
                    player1.aim_mode = [False, 0]

            # if the event is equal to stop, then set run to false an quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        draw_window(win, player1, player2)


run_game()

