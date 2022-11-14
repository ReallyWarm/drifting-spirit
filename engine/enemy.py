import pygame
from engine.graphic.animate import Animate

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, ani, state):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)
        self.ani = ani
        self.state = state

    def update(self, dt):
        self.image = self.ani[self.state].update(dt)

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

        super().__init__(pos, self.ani['idle'].image, self.ani, self.state)
    
    def attack(self, bullets, dt, stop_attack=False):
        pass

class Imp(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/imp-idle.png",(0,0,32,32), 9, pixel_jump=2, frames=25)}
        self.state = 'idle'
        self.attack_time = [0,180]

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image, self.ani, self.state)

    def attack(self, bullets, dt, stop_attack=False):
        if not stop_attack:
            self.attack_time[0] += 1
            if self.attack_time[0] >= self.attack_time[1] / dt:
                bullets.add([self.rect.centerx,self.rect.centery], 8, 1.5, 90, time=200, color=(175,60,40), particle=True)
                self.attack_time[0] = 0