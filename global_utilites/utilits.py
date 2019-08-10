# this python file includes a bunch of function which will be interesting for all objects in the game


def define_rect(rect_tuple):
    # (y, y, width, height)
    x = rect_tuple[0]
    y = rect_tuple[1]
    x2 = rect_tuple[0] + rect_tuple[2]
    y2 = rect_tuple[1] + rect_tuple[3]
    return x, y, x2, y2
