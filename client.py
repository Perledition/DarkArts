import pygame
from .objects.game_objects import Player


# set global window settings
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


# draw the Window which we want to display
def draw_window(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


# Defines the main loop which runs until the program gets stopped
def main():
    run = True
    player = Player(50, 50, 100, 100, (0, 255, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        # update the game window for each event // pygame specific
        for event in pygame.event.get():

            # if the event is equal to stop, then set run to false an quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        draw_window(win, player)

main()