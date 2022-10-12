import pygame
from engine.graphic.animate import Animate

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ani = {'run' : Animate("sprite/player-run.png", (0,0,24,32), 8, pixel_jump=2, frames=6),
                    'idle': Animate("sprite/player-idle.png",(0,0,24,32), 4, pixel_jump=2, frames=45)}
        self.aniType = 'run'
        self.image = self.ani['idle'].sprites[0]
        self.rect = self.image.get_rect(center = (50,50))

    def update(self, dt):
        self.image = self.ani[self.aniType].update(dt)