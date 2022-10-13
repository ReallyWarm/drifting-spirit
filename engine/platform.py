import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (100, 100))
 