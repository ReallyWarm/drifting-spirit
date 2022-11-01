import pygame
from engine.graphic.animate import Animate

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, ani, amount):
        super().__init__()
        self.ani = ani
        self.image = self.ani.image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)
        self.amount = amount
        self.ani_delay = [0, 60]

    def update(self, dt):
        self.ani_delay[0] += 1

        if self.ani_delay[0] >= self.ani_delay[1] / dt:
            if self.ani.ani_done:
                self.ani.reset()
                self.ani_delay[0] = 0

            self.image = self.ani.update(dt)

class ItemDash(Item):
    def __init__(self, name, pos, amount=1):
        # Animation and Image
        self.name = name
        ani = Animate("sprite/spirit-item.png",(0,0,24,24), 5, loop=False, frames=15)
        super().__init__(pos, ani, amount)

class ItemHealth(Item):
    def __init__(self, name, pos, amount=1):
        # Animation and Image
        self.name = name
        ani = Animate("sprite/spirit-item.png",(0,24,24,24), 5, loop=False, frames=15)

        super().__init__(pos, ani, amount)

class ItemScore(Item):
    def __init__(self, name, pos, amount=1):
        # Animation and Image
        self.name = name
        ani = Animate("sprite/spirit-item.png",(0,48,24,24), 5, loop=False, frames=15)

        super().__init__(pos, ani, amount)