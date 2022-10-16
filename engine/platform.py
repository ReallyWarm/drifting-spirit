import pygame

class PlatformSet():
    def __init__(self):
        self.data = {}

    def add(self, name, image_list):
        block = len(image_list)
        w, h = image_list[0].get_size()
        surf = pygame.Surface((w*block, h), pygame.SRCALPHA)
        for i, image in enumerate(image_list):
            surf.blit(image, (w*i,0))
        self.data[name] = surf

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, dt):
        pass