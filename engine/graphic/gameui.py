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
        self.normal_img.fill(color)
        self.normal_img.blit(text_surf, text_surf.get_rect(center=(width//2,height//2)))
        
        self.hover_img = self.normal_img.copy()
        self.overlay = pygame.Surface((width,height))
        self.overlay.fill((50,50,50))
        self.hover_img.blit(self.overlay, (0,0), special_flags=pygame.BLEND_RGB_ADD)
        
        self.rect = pygame.Rect(x, y, width, height)

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
