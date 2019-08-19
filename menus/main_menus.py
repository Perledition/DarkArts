# this file holds all the menus

# standard module imports
import os

# third party imports
import pygame

# game module imports
from settings.global_constants import window_heigth, window_width
from global_utilites.elements import Button
from global_utilites.utilits import in_rect, define_rect


class WindowManager:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("DarkArena")
        self.clock = pygame.time.Clock()
        self.width = window_width
        self.height = window_heigth
        self.win = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font('freesansbold.ttf', 115)


class MainMenu(WindowManager):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(os.path.join('images/', 'main_menu.png'))
        self.intro = True

    def draw_menu(self):
        self.win.blit(self.background, (0, 0))

    def start_screen(self):
        join_button = Button((46, 116, 130), 310, 536, 150, 50, 'Enter the Arena')
        while self.intro:
            self.clock.tick(60)

            # draw all elements
            self.draw_menu()
            join_button.draw(self.win)
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                rec = (join_button.x, join_button.y, join_button.x + join_button.width,
                       join_button.y + join_button.height)
                rec = define_rect(rec)

                if event.type == pygame.QUIT:
                    self.intro = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if in_rect(pos, rec):
                        print('Start Game')

                if event.type == pygame.MOUSEMOTION:

                    if in_rect(pos, rec):
                        join_button.color = (42, 43, 46)
                    else:
                        join_button.color = (46, 116, 130)

    def text_objects(self, text):
        text_surface = self.font.render(text, True, (21, 99, 194))
        return text_surface, text_surface.get_rect()

    def message_display(self, text):
        text_surf, text_rect = self.text_objects(text)
        text_rect.center = ((self.width / 2), (self.height / 2))
        self.win.blit(text_surf, text_rect)
        pygame.display.update()


class HoseSelection(WindowManager):
    pass


class WandSeleciton(WindowManager):
    pass


p = MainMenu()
p.start_screen()