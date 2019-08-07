import pygame
import os
from network import Network
from settings.global_constants import window_heigth, window_width

# set global window settings
width = window_width
height = window_heigth
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
# print(pygame.display.list_modes())

# defines lists of images for the walking animation
SKIN_PATH = 'objects/statics/player/skin'  # get parent folder
walk_right = [pygame.image.load(os.path.join(SKIN_PATH, img)) for img in
                   ['R{}.png'.format(x) for x in range(1, 5)]]
walk_left = [pygame.image.load(os.path.join(SKIN_PATH, img)) for img in
                  ['L{}.png'.format(x) for x in range(1, 5)]]
char = pygame.image.load(os.path.join(SKIN_PATH, 'standing.png'))


def draw_player(plr, window):
    # if we move in the left direction display the image by index of walk_count // same for right
    if plr.position_map[0]:
        window.blit(walk_left[plr.walk_count], (plr.x, plr.y))

    elif plr.position_map[1]:
        window.blit(walk_right[plr.walk_count], (plr.x, plr.y))

    elif plr.position_map[2] or plr.position_map[3]:
        window.blit(char, (plr.x, plr.y))

    else:
        window.blit(char, (plr.x, plr.y))

    pygame.draw.rect(window, (255, 0, 0), plr.hitbox, 2)


# draw the Window which we want to display
def draw_window(window, player, player2):
    win.fill((255, 255, 255))

    draw_player(player, window)
    draw_player(player2, window)

    # draw all the spells player one has casted
    for sp1 in player.spells:
        sp1.update()
        sp1.draw(window)

    for sp2 in player2.spells:
        sp2.update()
        sp2.draw(window)

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

            # if the event is equal to stop, then set run to false an quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        draw_window(win, player1, player2)


run_game()

