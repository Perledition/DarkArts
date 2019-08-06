import pygame
from network import Network


# set global window settings
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


# draw the Window which we want to display
def draw_window(window, player, player2):
    win.fill((255, 255, 255))
    player.draw(window)
    player2.draw(window)
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

