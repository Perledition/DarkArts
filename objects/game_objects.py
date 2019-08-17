# find all the Game objects in here
from .spells import *
from settings.global_constants import window_heigth, window_width

# TODO: Create exchangeable spell casts


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
        self.speed = 50 * 60/1000
        self.x_vel = 0    # defines the speed of the object when pressing key
        self.y_vel = 0  # defines the speed of the object when pressing key

        self.direction = 0  # defines in which the direction the player is going
        self.spells = []  # includes all spells created for the character
        self.walk_count = 0  # keeps track of the steps - needed for the sprites

        # this defines the player conditions
        self.health = attributes[0]
        self.magic = attributes[1]
        self.magic_available = attributes[1]
        self.hitbox = (self.x + 20, self.y + 10, 28, 50)
        self.aim_mode = [False, 0]
        self.spell_collection = {1: Stupor(round(self.x + self.width // 2), round(self.y + self.height // 2), 6, (0, 255, 0), 1, self.id)}

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update_spell(self):
        """
        This function loop over all existing spells the player has casted and removes them the list
        whenever the attribute damage_dealt was set to True. The update happens within the main loop
        of the client. Nevertheless has the spell to be removed on the player object. In case the spell
        did not hit an enemy object, it will be removed when it leave the battlefield.
        :return: None - it does have a return value
        """

        # loop over all objects in the spells list
        for spell in self.spells:

            # remove the spell form the list, in case it dealt damage to an enemy - spell is not needed anymore
            if spell.damage_dealt:
                self.spells.pop(self.spells.index(spell))

            # remove the spell in case it did not hurt anyone but is also outside of the battlefield
            if (spell.x > window_width) or (spell.x < 0) or (spell.y > window_heigth) or (spell.y < 0):
                self.spells.pop(self.spells.index(spell))

    def update(self):
        """
        This function updates important counts and minor parts. Is starts with the rectangle position of the player.
        However, it will also return the walk count to zero is case it reached the limit of 4. This is important,
        because the spites only count to 4 and it would return an index out of range error. Also the function checks
        for the current spells and returns the magic load.
        :return:  None. The function has no need to return a value
        """
        # update the players rectangle position which is the baseline for displaying and moving the player object
        self.rect = (self.x, self.y, self.width, self.height)

        # set the walk count back in case it reached the index limit
        #if self.walk_count + 1 >= 4:
        #    self.walk_count = 0

        # check if spells need to be removed from the spells list
        self.update_spell()

        # fill up the magic energy
        if self.magic_available < self.magic:
            self.magic_available += 1

    def cast_spell(self, spell_to_cast):
        """
        This function simply takes a spell object and appends it to the spells list.
        However, it will also reduce the magic by the magic costs of the spell
        :param spell_to_cast: (object): the spell which needs to be append to the list
        :return: None - The function needs no return value
        """
        self.spells.append(spell_to_cast)
        self.magic_available -= spell_to_cast.magic_cost

    def hit(self, damage):
        """
        In case the player was hit by an enemy spell the function will reduce the players health by the dealt damage.
        Be aware, that this function will only be called in the main loop of the client. The dealt damage depends
        on the spell of the enemy
        :param damage: (int): Number of health by which the players health gets reduced
        :return: None - Function needs no return value
        """
        self.health -= damage

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

    def update_aim_mode(self):
        """
        This function creates a lane which indicates the direction in which a spell will fly. This is supports the
        to aim in the right direction. This means that the player will not be able to choose a new direction to walk
        to as long as the aim mode is on. The lane points into the direction of the mouse cursor.
        :return:
        """
        pass

    def update_key_presses(self):
        """
        This function updates all pressed keys. This is relevant to cast new spells and to check for
        player actions beside the movement.

        :return: Does not return anything
        """

        # keys is a list of keys and if they are pressed the value will be a one
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            if self.magic_available >= self.spell_collection[1].magic_cost:
                self.aim_mode = [True, 1]

    def move(self):
        """
        This function handles the whole movement behavior of the player and is therefore pretty important for the whole
        game. In a nutshell do we compare the starting vector with the end vector. The speed is set by the speed
        attribute. This get multiplied with the x and y velocity for each data point x and y. But before that we
        create an direction indicator to observe the behavior of the movement.

        At the end we just update all other behaviors as well, like health, magic, walk count, hitbox and key presses
        which lead to casting spells.

        :return: Does not return anything
        """

        # this is meant to calculate the direction of the movement
        xd, yd = self.get_direct_indicators()

        # check if the target is already reached and if the distance is larger then a movement
        if (self.target[0] - self.x) != 0 and abs(self.target[0] - self.x) > self.x_vel:

            # update the current x position with predefined movement * direction indicator
            # x_vel gets predefined in the client for each new target vector
            self.x += xd * self.x_vel

            # update the walk count this you moved in this function
            # self.walk_count += 1

        # in case the distance is smaller then one move, just return the rest of the distance
        else:
            self.x += (self.target[0] - self.x)
            # self.walk_count += 1

        # same as above but just for the y coordinate
        if (self.target[1] - self.y) != 0 and abs(self.target[1] - self.y) > self.y_vel:
            self.y += yd * self.y_vel
            # self.walk_count += 1
        else:
            self.y += (self.target[1] - self.y)
            # self.walk_count += 1

        # update the hitbox. It is important to move the hitbox with the player. So the player can be damaged.
        self.hitbox = (self.x + 20, self.y + 10, 28, 50)

        # update other key presses for castings portions and so on
        self.update_key_presses()

        # update the player attributes
        self.update()






