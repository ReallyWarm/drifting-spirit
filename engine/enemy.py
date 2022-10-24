import pygame
from engine.graphic.animate import Animate

class ImpEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Animation and Image
        self.ani = {'idle': Animate("sprite/imp-idle.png",(0,0,32,32), 9, pixel_jump=2, frames=25)}
        self.image = self.ani['idle'].image
        self.rect = self.image.get_rect(topleft = pos)
        self.state = 'idle'

        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)
    
    def update(self, dt):
        image = self.ani[self.state].update(dt)
        if self.rect.centerx > 128:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)