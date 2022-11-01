import pygame
from engine.graphic.animate import Animate

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)

class Ghost(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/ghost-idle.png",(0,0,32,32), 4, pixel_jump=2, frames=25)}
        self.state = 'idle'

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image)

    def update(self, dt):
        self.image = self.ani[self.state].update(dt)

class Imp(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/imp-idle.png",(0,0,32,32), 9, pixel_jump=2, frames=25)}
        self.state = 'idle'

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image)
    
    def update(self, dt):
        self.image = self.ani[self.state].update(dt)