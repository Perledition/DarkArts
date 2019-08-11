# this python file includes a bunch of function which will be interesting for all objects in the game
import math
import numpy as np


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





