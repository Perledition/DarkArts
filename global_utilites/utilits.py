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









