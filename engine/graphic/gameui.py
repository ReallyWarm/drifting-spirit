# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_ui_elements.md

import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, font, text):
        super().__init__()
        self.set_button(x, y, width, height, color, font, text)
        self.image = self.normal_img
        self.clicked = False

    def set_button(self, x, y, width, height, color, font, text):
        text_surf = font.render(text, True, (255,255,255))

        self.normal_img = pygame.Surface((width,height))
        self.rect = self.normal_img.get_rect(topleft=(x, y))

        self.normal_img.fill(color)
        self.normal_img.blit(text_surf, text_surf.get_rect(center=(width//2,height//2)))
        border_color = (max(color[0]-80,0), max(color[1]-80,0), max(color[2]-80,0))
        pygame.draw.rect(self.normal_img, border_color, pygame.Rect(0,0,width,height),4)
        
        self.hover_img = self.normal_img.copy()
        self.overlay = pygame.Surface((width,height))
        self.overlay.fill((50,50,50))
        self.hover_img.blit(self.overlay, (0,0), special_flags=pygame.BLEND_RGB_ADD)

    def get_clicked(self):
        click = self.clicked
        self.clicked =  False
        return click

    def update(self, event_list):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if hover:
            self.image = self.hover_img
        else:
            self.image = self.normal_img
        for event in event_list:
            if hover and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

class TextInput(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, font, preview='', max_text=10):
        super().__init__()
        self.color = color
        self.font = font
        self.font_offset = self.font.get_height() + self.font.get_descent()*2
        self.preview = preview
        self.text = ''
        self.max_text = max_text
        self.show_preview = True
        self.clicked =  False
        self.active = False

        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.render_text()

    def get_clicked(self):
        click = self.clicked
        self.clicked =  False
        return click

    def get_input(self):
        text = self.text
        self.text = ''
        self.show_preview = True
        self.active = False
        self.render_text()
        return text

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.active = self.rect.collidepoint(pygame.mouse.get_pos())
                if self.active:
                    self.clicked = True
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_text:
                        self.text += event.unicode

                self.show_preview = False if self.text else True
                self.render_text()

    def render_text(self):
        self.image.fill(self.color)
        if self.show_preview:
            text_surf = self.font.render(self.preview, True, (min(self.color[0]+80,255), min(self.color[1]+80,255), min(self.color[2]+80,255)))
        else:
            text_surf = self.font.render(self.text, True, (255,255,255))
        self.image.blit(text_surf, text_surf.get_rect(topleft=(self.font_offset, (self.rect.height-self.font.get_ascent())//2)))
        pygame.draw.rect(self.image, (255,255,255), self.image.get_rect().inflate(-self.font_offset/2, -self.font_offset/2), self.font_offset//4)

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

class HealthUI(pygame.sprite.Sprite):
    def __init__(self, pos, rect, image):
        super().__init__()
        self.pos = pos
        self.rect = rect
        self.image = image.copy()
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.show = True

    def update(self, player):
        if self.pos > player.health + player.rg_health:
            self.show = False

class PowerUI(pygame.sprite.Sprite):
    def __init__(self, type, pos, rect, image_state):
        super().__init__()
        self.type = type
        self.pos = pos
        self.rect = rect
        self.image_state = image_state.copy()

        for i in range(len(self.image_state)):
            self.image_state[i] = pygame.transform.scale(self.image_state[i], self.rect.size)

        self.recharge = True
        self.image = self.image_state[0]

    def update(self, player):
        if self.pos > player.power_amount:
            self.recharge = False
            if self.type == 1:
                self.image = self.image_state[1]
        else:
            self.recharge = True
            self.image = self.image_state[0]
