# this file holds all the menus

# standard module imports
import os
import random

# third party imports
import pygame

# game module imports
from settings.global_constants import window_heigth, window_width
from global_utilites.elements import Button, InputBox
from global_utilites.utilits import in_rect, define_rect


class SceneBase:
    def __init__(self):
        self.next = self
        pygame.init()

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


# In this section most of the introduction menus are defined.

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.font = pygame.font.Font('freesansbold.ttf', 115)
        self.background = pygame.image.load(os.path.join('images/', 'menu_bg.jpg'))
        self.login = pygame.image.load(os.path.join('images/', 'login_box.png'))
        self.join_button = Button((46, 116, 130), (42, 43, 46), 250, 606, 150, 30, 'Enter the Arena')
        self.username = InputBox(130, 470, 150, 30)
        self.password = InputBox(130, 540, 150, 30)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            pos = pygame.mouse.get_pos()
            rec = define_rect(self.join_button.button_config())

            for box in [self.username]:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_rect(pos, rec):
                    print('Start Game')
                    self.SwitchToScene(HousesScene())

            if event.type == pygame.MOUSEMOTION:
                if in_rect(pos, rec):
                    self.join_button.hover(True)
                else:
                    self.join_button.hover(False)

        for box in [self.username]:
            box.update()

    def Update(self):
        pass

    def Render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.login, (0, 0))
        self.join_button.draw(screen)
        self.username.draw(screen)
        self.password.draw(screen)


class HousesScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.griff_img = [pygame.image.load(os.path.join('images/', x)) for x in ['griff_color.png', 'griff_gray.png']]
        self.huff_img = [pygame.image.load(os.path.join('images/', x)) for x in ['huff_color.png', 'huff_gray.png']]
        self.rave_img = [pygame.image.load(os.path.join('images/', x)) for x in ['rave_color.png', 'rave_gray.png']]
        self.slys_img = [pygame.image.load(os.path.join('images/', x)) for x in ['slys_color.png', 'slys_gray.png']]

        house_list = ['{}_attr.png'.format(i) for i in ['griff', 'slys', 'huff', 'rave']]
        self.attributes = [pygame.image.load(os.path.join('images/', x)) for x in house_list]
        self.gradient = pygame.image.load(os.path.join('images/', 'gradient.png'))
        self.last_hover = 0

        w, h = pygame.display.get_surface().get_size()
        bw = w / 4
        b_height = h - 50  # 50 pixels are needed to display the text

        # define button
        self.r_button = Button((56, 54, 54), (13, 96, 166), 0, 0, bw, b_height, 'Ravenclaw', self.rave_img[1],
                          self.rave_img[0], text_size=40)
        self.h_button = Button((56, 54, 54), (227, 190, 2), 1 * bw, 0, bw, b_height, 'Huffelpuff', self.huff_img[1],
                          self.huff_img[0], text_size=40)
        self.g_button = Button((56, 54, 54), (184, 22, 22), 2 * bw, 0, bw, b_height, 'Griffendor', self.griff_img[1],
                          self.griff_img[0], text_size=40)
        self.s_button = Button((56, 54, 54), (8, 156, 16), 3 * bw, 0, bw, b_height, 'Slytherin', self.slys_img[1],
                          self.slys_img[0], text_size=40)

    def ProcessInput(self, events, pressed_keys):
        pos = pygame.mouse.get_pos()
        r_rect = define_rect(self.r_button.button_config())
        g_rect = define_rect(self.g_button.button_config())
        h_rect = define_rect(self.h_button.button_config())
        s_rect = define_rect(self.s_button.button_config())

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_rect(pos, g_rect):
                    print('you picked Griffendor')
                    self.SwitchToScene(WandScene())

                if in_rect(pos, r_rect):
                    self.SwitchToScene(WandScene())
                    print('you picked Ravenclaw')

                if in_rect(pos, h_rect):
                    self.SwitchToScene(WandScene())
                    print('you picked Huffelpuff')

                if in_rect(pos, s_rect):
                    self.SwitchToScene(WandScene())
                    print('you picked Slytherin')

            if event.type == pygame.MOUSEMOTION:

                if in_rect(pos, g_rect):
                    self.g_button.hover(True)
                    if self.last_hover != 1:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 1
                else:
                    self.g_button.hover(False)

                if in_rect(pos, r_rect):
                    self.r_button.hover(True)
                    if self.last_hover != 2:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 2
                else:
                    self.r_button.hover(False)

                if in_rect(pos, h_rect):
                    self.h_button.hover(True)
                    if self.last_hover != 3:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 3
                else:
                    self.h_button.hover(False)

                if in_rect(pos, s_rect):
                    self.s_button.hover(True)
                    if self.last_hover != 4:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 4
                else:
                    self.s_button.hover(False)

    def Update(self):
        pass

    def Render(self, screen):
        self.r_button.draw(screen)
        self.g_button.draw(screen)
        self.h_button.draw(screen)
        self.s_button.draw(screen)

        screen.blit(self.gradient, (0, 0))


class WandScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        wand_picks = ['wand{}.png'.format(random.randint(1, 12)) for x in range(0, 3)]
        self.wand1_img = [pygame.image.load(os.path.join('images/wands/', x)) for x in [wand_picks[0], wand_picks[0]]]
        self.wand2_img = [pygame.image.load(os.path.join('images/wands/', x)) for x in [wand_picks[1], wand_picks[1]]]
        self.wand3_img = [pygame.image.load(os.path.join('images/wands/', x)) for x in [wand_picks[2], wand_picks[2]]]

        self.gradient = pygame.image.load(os.path.join('images/', 'gradient.png'))
        self.wand_index = random.choice([1, 2, 3])
        self.picked = False
        self.last_hover = 0

        w, h = pygame.display.get_surface().get_size()
        bw = w / 3
        b_height = h - 50  # 50 pixels are needed to display the text

        # define button
        self.wand1 = Button((56, 54, 54), (66, 64, 64), 0, 0, bw, b_height, image=self.wand1_img[1], h_image=self.wand1_img[0], center=True)
        self.wand2 = Button((56, 54, 54), (66, 64, 64), 1 * bw, 0, bw, b_height, image=self.wand2_img[1], h_image=self.wand2_img[0], center=True)
        self.wand3 = Button((56, 54, 54), (66, 64, 64), 2 * bw, 0, bw, b_height, image=self.wand3_img[1], h_image=self.wand3_img[0], center=True)

    def ProcessInput(self, events, pressed_keys):
        pos = pygame.mouse.get_pos()
        w1_rect = define_rect(self.wand1.button_config())
        w2_rect = define_rect(self.wand2.button_config())
        w3_rect = define_rect(self.wand3.button_config())

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_rect(pos, w1_rect):
                    if self.wand_index is 1:
                        self.picked = True
                        print('you found your wand, or did the wand found you?!')
                    else:
                        print('Ohhhh noo. This is the right one for you')

                if in_rect(pos, w2_rect):
                    if self.wand_index is 2:
                        self.picked = True
                        print('you found your wand, or did the wand found you?!')
                    else:
                        print('Ohhhh noo. This is the right one for you')

                if in_rect(pos, w3_rect):
                    if self.wand_index is 3:
                        self.picked = True
                        print('you found your wand, or did the wand found you?!')
                    else:
                        print('Ohhhh noo. This is the right one for you')

            if event.type == pygame.MOUSEMOTION:

                if in_rect(pos, w1_rect):
                    self.wand1.hover(True)
                    if self.last_hover != 1:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 1
                else:
                    self.wand1.hover(False)

                if in_rect(pos, w2_rect):
                    self.wand2.hover(True)
                    if self.last_hover != 2:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 2
                else:
                    self.wand2.hover(False)

                if in_rect(pos, w3_rect):
                    self.wand3.hover(True)
                    if self.last_hover != 3:
                        pygame.mixer.music.load('sounds/button.mp3')
                        pygame.mixer.music.play(0)
                        self.last_hover = 3
                else:
                    self.wand3.hover(False)

    def Update(self):
        pass

    def Render(self, screen):
        self.wand1.draw(screen)
        self.wand2.draw(screen)
        self.wand3.draw(screen)

        screen.blit(self.gradient, (0, 0))


class InGameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass


def run_game(fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_heigth))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)


run_game(60, TitleScene())