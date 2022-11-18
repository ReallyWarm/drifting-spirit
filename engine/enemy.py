import pygame
from engine.graphic.animate import Animate

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, ani, state, attack_time=None, attack_angle=[90]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)
        self.ani = ani
        self.state = state
        self.attacked = False
        self.attack_time = attack_time
        self.attack_angle = attack_angle

    def attack(self, bullets, dt):
        if self.attack_time is not None:
            self.attacked = False
            self.attack_time[0] += 1
            if self.attack_time[0] >= self.attack_time[1] / dt:
                for angle in self.attack_angle:
                    bullets.add([self.rect.centerx-4,self.rect.centery+4], 8, 1.5, angle, time=200, color=(175,60,40), particle=True)
                self.attack_time[0] = 0
                self.attacked = True

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

class Bird(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/bird-idle.png",(0,0,32,32), 7, pixel_jump=2, frames=6)}
        self.state = 'idle'
        self.attack_time = [100,140]
        self.attack_angle = [90]

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image, self.ani, self.state, self.attack_time, self.attack_angle)


class Imp(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/imp-idle.png",(0,0,32,32), 9, pixel_jump=2, frames=25)}
        self.state = 'idle'
        self.attack_time = [120,160]
        self.attack_angle = [60,120]

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image, self.ani, self.state, self.attack_time, self.attack_angle)

class Mage(Enemy):
    def __init__(self, name, pos):
        # Animation and Image
        self.name = name
        self.ani = {'idle': Animate("sprite/mage-idle.png",(0,0,32,32), 8, pixel_jump=2, frames=10)}
        self.state = 'idle'
        self.attack_time = [160,200]
        self.attack_angle = [90,35,145]

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image, self.ani, self.state, self.attack_time, self.attack_angle)

    def set_attack_angle(self, angle):
        self.attack_angle = angle
        self.attack_angle.append(angle[0]-55)
        self.attack_angle.append(angle[0]+55)