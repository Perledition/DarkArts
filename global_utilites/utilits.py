# this python file includes a bunch of function which will be interesting for all objects in the game

# standard module imports
import math

# third party module imports
import pygame

# import project module imports
from objects.statics.sprites import char, arena
from objects.boundries import Wall


def define_rect(rect_tuple):
    # (y, y, width, height)
    x = rect_tuple[0]
    y = rect_tuple[1]
    x2 = rect_tuple[0] + rect_tuple[2]
    y2 = rect_tuple[1] + rect_tuple[3]
    return x, y, x2, y2


def in_rect(point, rect_tuple):
    x, y = point
    x1, y1, x2, y2 = rect_tuple
    if (x > x1) and (x < x2) and (y > y1) and (y < y2):
        return True
    else:
        return False


def vector_length(x, y):
    return math.sqrt(x**2 + y**2)


def pythagoras(start, end, distance):
    """
    This function is basic Trigonometry. The function takes the starting point and the cursor position and
    calculates a point on this vector which is in the desired distance to the starting point.

    :param start: (tuple): (x, y) coordinates from the starting object
    :param end: (tuple): (x, y) coordinates, normally of the mouse cursor.
    :param distance: (int): defines the distance on the x-axis.
    :return: (tuple): returns the end point of the vector in the right distance.
    """

    # since cos(a) / adjacent defines the hypothenuse we need to calculate the cos(a) first
    # cos(a) = vec(a)*vec(b)/(|a|+|b|)
    # transform direction vectors to position vector
    # a = end-start // b = (x of a, y=0)
    x_a = end[0] - start[0]
    y_a = end[1] - start[1]
    ab = x_a**2 + y_a

    # calculate the length of each vector
    length_a = vector_length(x_a, y_a)
    length_b = vector_length(x_a, 0)

    # calculate cos(a)
    cos = ab/(length_a + length_b)

    # hypothenuse = cos(a)/ adjacent (distance)
    hypo = cos/distance

    # return the step size for x and y calculated by c2 = a2 - b2 // pythagoras
    return distance, math.sqrt(hypo**2 + distance**2)


# Find the angle that the ball hits the ground at
def find_angle(start, pos):
    sX = start[0]
    sY = start[1]

    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))

    except ZeroDivisionError:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


def barycentric_method(p1, p2, p3, p):
    # p[0] = x of p, p[1] = y of p p is a tuple
    denom = ((p2[1] - p3[1])*(p1[0] - p3[0]) + (p3[0] - p2[0])*(p1[1] - p3[1]))
    nom_a = ((p2[1] - p3[1])*(p[0] - p3[0]) + (p3[0] - p2[0])*(p[1] - p3[1]))
    nom_b = ((p3[1] - p1[1])*(p[0] - p3[0]) + (p1[0] - p3[0])*(p[1] - p3[1]))
    a = nom_a / denom
    b = nom_b / denom
    c = 1 - a - b
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1


def define_unique_direction(angle):
    """
    this function takes the angle as degree from an atan2 function and check in which direction
    the vector is pointing. Therefore, each area has it's predefined angle area. The purpose of the
    function is to return a unique direction for the object to classify which sprite needs to be displayed.
    the return is based on this index mapping:
    0: up, 1: up right, 2: right, 3: down right, 4: down, 5: down left, 6: left, 7: up left

    :param angle: (float): e.g 45.0 for 45° of slope angle
    :return: (int): the int will the the index for list of sprites which has to be displayed
    """
    if 112.5 >= angle > 67.5:
        return 0

    elif 67.5 >= angle > 22.5:
        return 1

    elif (22.5 >= angle >= 0) or (0 >= angle > -22.5):
        return 2

    elif -22.5 >= angle > -67.5:
        return 3

    elif -67.5 >= angle > -112.5:
        return 4

    elif -112.5 >= angle > -157.5:
        return 5

    elif (-157.5 >= angle > -180.0) or (180 >= angle > 157.5):
        return 6

    elif 157.5 >= angle > 112.5:
        return 7


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
    window.blit(arena, (0, 0))

    draw_player(player, window)
    draw_player(player2, window)

    # draw all the spells player one has casted
    for sp in player.spells + player2.spells:
        sp.update(spell_hit(player, sp, player2))
        sp.draw(window)

    # Draw the walls and boundaries
    for x in range(10, 400):
        Wall(x, 20).draw(window)

    # check if the aim mode needs to be drawn
    if player.aim_mode[0]:

        start_pos = (round(player.x + player.width // 2), round(player.y + player.height // 2))

        angle = find_angle(start_pos, pygame.mouse.get_pos())
        line = (round(start_pos[0] + (math.cos(angle) * 150)), round(start_pos[1] - (math.sin(angle) * 150)))

        pygame.draw.line(window, (155, 23, 112), start_pos, line, 10)

    pygame.display.update()







