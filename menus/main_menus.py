# this file holds all the menus

# standard module imports
import os

# third party imports
import pygame

# game module imports
from settings.global_constants import window_heigth, window_width
from global_utilites.elements import Button, InputBox
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
        self.stage = 0


class MainMenu(WindowManager):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(os.path.join('images/', 'main_menu.png'))
        self.intro = True

    def draw_menu(self):
        self.win.blit(self.background, (0, 0))

    def start_screen(self):
        join_button = Button((46, 116, 130), (42, 43, 46), 150, 536, 150, 50, 'Enter the Arena')
        username = InputBox(150, 500, 150, 30)
        while self.intro:
            self.clock.tick(60)

            # draw all elements
            self.draw_menu()
            join_button.draw(self.win)
            username.draw(self.win)
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                rec = define_rect(join_button.button_config())

                if event.type == pygame.QUIT:
                    done = True

                for box in [username]:
                    box.handle_event(event)

                if event.type == pygame.QUIT:
                    self.intro = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if in_rect(pos, rec):
                        print('Start Game')

                if event.type == pygame.MOUSEMOTION:
                    if in_rect(pos, rec):
                        join_button.hover(True)
                    else:
                        join_button.hover(False)

            for box in [username]:
                box.update()


class HoseSelection(WindowManager):

    def __init__(self):
        super().__init__()
        self.selected = False
        self.griff_img = [pygame.image.load(os.path.join('images/', x)) for x in ['griff_color.png', 'griff_gray.png']]
        self.huff_img = [pygame.image.load(os.path.join('images/', x)) for x in ['huff_color.png', 'huff_gray.png']]
        self.rave_img = [pygame.image.load(os.path.join('images/', x)) for x in ['rave_color.png', 'rave_gray.png']]
        self.slys_img = [pygame.image.load(os.path.join('images/', x)) for x in ['slys_color.png', 'slys_gray.png']]

        house_list = ['{}_attr.png'.format(i) for i in ['griff', 'slys', 'huff', 'rave']]
        self.attributes = [pygame.image.load(os.path.join('images/', x)) for x in house_list]
        self.gradient = pygame.image.load(os.path.join('images/', 'gradient.png'))

    def house_screen(self):
        w, h = pygame.display.get_surface().get_size()
        bw = w/4
        b_height = h - 50  # 50 pixels are needed to display the text

        # define button
        r_button = Button((56, 54, 54), (13, 96, 166), 0, 0, bw, b_height, 'Ravenclaw', self.rave_img[1], self.rave_img[0])
        h_button = Button((56, 54, 54), (227, 190, 2), 1 * bw, 0, bw, b_height, 'Huffelpuff', self.huff_img[1], self.huff_img[0])
        g_button = Button((56, 54, 54), (184, 22, 22), 2 * bw, 0, bw, b_height, 'Griffendor', self.griff_img[1], self.griff_img[0])
        s_button = Button((56, 54, 54), (8, 156, 16), 3 * bw, 0, bw, b_height, 'Slytherin', self.slys_img[1], self.slys_img[0])
        self.clock.tick(60)

        while not self.selected:
            # font = pygame.font.SysFont('Arial', 20)
            # text = font.render('Pick your house', 1, (255, 255, 255))
            # self.win.blit(text, (
            # self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

            r_button.draw(self.win)
            g_button.draw(self.win)
            h_button.draw(self.win)
            s_button.draw(self.win)

            self.win.blit(self.gradient, (0, 0))
            pygame.display.update()

            pos = pygame.mouse.get_pos()
            r_rect = define_rect(r_button.button_config())
            g_rect = define_rect(g_button.button_config())
            h_rect = define_rect(h_button.button_config())
            s_rect = define_rect(s_button.button_config())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.selected = True
                    pygame.quit()
                    quit()

                # check in which button the the mouse is and trigger action on click and create hover
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if in_rect(pos, g_rect):
                        print('you picked Griffendor')

                    if in_rect(pos, r_rect):
                        print('you picked Ravenclaw')

                    if in_rect(pos, h_rect):
                        print('you picked Huffelpuff')

                    if in_rect(pos, s_rect):
                        print('you picked Slytherin')

                if event.type == pygame.MOUSEMOTION:

                    if in_rect(pos, g_rect):
                        g_button.hover(True, 'Griffendor members are brave and strong:\n +5% life\n +2% damage\n -2% magic refresh rate')
                        self.win.blit(self.attributes[0], (100, 200))
                    else:
                        g_button.hover(False)

                    if in_rect(pos, r_rect):
                        r_button.hover(True, 'Ravenclaw members are intelligent and creative:\n +5% magic refresh rate\n +2% stronger shild\n -2% life')
                    else:
                        r_button.hover(False)

                    if in_rect(pos, h_rect):
                        h_button.hover(True, 'Huffelpuff members are patience and loyal:\n +5% life\n +2% stronger shild\n -2% damage')
                    else:
                        h_button.hover(False)

                    if in_rect(pos, s_rect):
                        s_button.hover(True, 'Slytherin members are ambitious and cunning:\n +5% damage hit\n +2% critical hit\n -2% life')
                    else:
                        s_button.hover(False)


class WandSelection(WindowManager):
    pass


p = HoseSelection()
p.house_screen()

#p = MainMenu()
#p.start_screen()