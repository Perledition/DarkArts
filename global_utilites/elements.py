import os
import pygame


class Button:

    def __init__(self, color, h_color, x, y, width, height, text='', image=None, h_image=None, text_size=14, text_color=(255, 255, 255)):
        self.color = color
        self.hover_color = h_color
        self.hover_image = h_image
        self.display_color = color
        self.text_color = tuple(int(x - x/2) for x in self.color)
        self.text_display_color = self.text_color
        self.text_hover_color = text_color
        self.text_size = text_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.display_image = image
        self.textbox = False
        self.textbox_text = ''
        self.sound = pygame.mixer.music.load(os.path.join('sounds/', 'button.mp3'))

    def draw(self, win, outline=None):
        """
        This method draws the button
        :param win: window in which the button has to be displayed.
        :param outline: defines if the button should have a outline
        """
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.display_color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont('Arial', self.text_size)
        text = font.render(self.text, 1, self.text_display_color)
        if self.text != '':
            # display the text in the center of the rect
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        if self.display_image is not None:
            x = self.x + (self.width/2 - self.image.get_width()/2)
            y = self.y + (self.height/2 - self.image.get_height() - text.get_height())
            win.blit(self.display_image, (x, y))

        if self.textbox:
            txy = self.height/2 + self.height/10 # the text box will be placed below the Image
            pygame.draw.rect(win, (0, 0, 0), (self.x, txy, self.width, self.height/3), 0)
            hover_text = font.render(self.textbox_text, 1, (255, 255, 255))
            win.blit(hover_text, (self.x + (self.width/2 - hover_text.get_width()/2), txy + hover_text.get_height()*3))

    def hover_text_up(self):
        self.textbox = True

    def hover(self, mode, hover_text=''):
        if mode:
            self.display_color = self.hover_color
            self.text_display_color = self.text_hover_color
            self.sound.play(0)
            if self.hover_image is not None:
                self.display_image = self.hover_image

            # if hover_text != '':
                # self.textbox_text = hover_text
                #self.textbox = True

        else:
            self.display_color = self.color
            self.display_image = self.image
            self.text_display_color = self.text_color
            self.textbox = False

    def button_config(self):
        return self.x, self.y, self.width, self.height


# TODO: Create a multi line surface
class MultiLineTextBox:

    def __init_(self, text, rect):
        self.text = text
        self.box = rect

    def text_to_portions(self):
        pass


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (42, 43, 46)
        self.text = text
        self.txt_surface = pygame.font.SysFont('Arial', 20).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color if self.active else (46, 116, 130)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.SysFont('Arial', 20).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # display solid ground
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.

        pygame.draw.rect(screen, self.color, self.rect, 2)
