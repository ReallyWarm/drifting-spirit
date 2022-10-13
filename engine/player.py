import pygame
from engine.graphic.animate import Animate
from engine.graphic.particlelist import ParticleList

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ani = {'run' : Animate("sprite/player-run.png", (0,0,24,32), 8, pixel_jump=2, frames=3),
                    'idle': Animate("sprite/player-idle.png",(0,0,24,32), 4, pixel_jump=2, frames=45),
                    'fall': Animate("sprite/player-fall.png",(0,0,24,32), 1),
                    'jump': Animate("sprite/player-jump.png",(0,0,24,32), 1)}
        self.image = self.ani['idle'].image
        self.rect = self.image.get_rect(midbottom = (100,50))

        self.vfx = ParticleList()
        self.vfx.new_type('candle',1,[1,(1,2),(245,295), 5, 0.2, (0,-1.5),(204,255,255), (0,20,20), False], 0)

        self.state = 'idel'
        self.face_right = True
        self.moveL = False
        self.moveR = False
        self.jumped = False
        
        self.direction = pygame.Vector2(0,0)
        self.pos = pygame.Vector2(self.rect.midbottom)
        self.vel = pygame.Vector2(0,0)
        self.acc = pygame.Vector2(0,0)

    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.moveL = True
                if event.key == pygame.K_d:
                    self.moveR = True
                if event.key == pygame.K_j:
                    self.jumped = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.moveL = False
                if event.key == pygame.K_d:
                    self.moveR = False

    def update(self, dt):
        self.move(dt)

        if self.vel.y > 0:
            self.state = 'fall'
        elif self.vel.y < 0:
            self.state = 'jump'
        elif self.vel.x != 0:
            self.state = 'run'
        else:
            self.state = 'idle'

        image = self.ani[self.state].update(dt)
        if self.face_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        mid_x, top_y = self.rect.midtop
        if self.state == 'idle' and self.ani['idle'].image_num != 3:
            top_y += 2
        self.vfx.add('candle', [mid_x, top_y], dt)
        self.vfx.update(dt)

    def move(self, dt):
        # Max speed = acc / fric
        acc = 0.6
        fric = -0.2
        max_y = 6.5
        self.acc = pygame.Vector2(0,0.2*dt)

        # Direction
        if self.moveR and self.moveL:
            self.direction.x = 0
        elif self.moveR:
            self.face_right = True
            self.direction.x = 1
        elif self.moveL:
            self.face_right = False
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.jumped:
            self.vel.y = -5.5 * dt
            self.jumped = False

        # Running
        self.acc.x = self.direction.x * acc * dt
        self.acc.x += self.vel.x * fric
        self.vel += self.acc * dt
        self.vel.y = max_y * dt if self.vel.y > max_y * dt else self.vel.y
        self.pos += (self.vel + 0.5 * self.acc)

        # Stopping
        if self.vel.x < 0.2 * dt and self.vel.x > -0.2 * dt:
            self.vel.x = 0

        # Collide map
        offset_p = self.rect.width//2
        if self.pos.x + offset_p > 256:
            self.pos.x = 256 - offset_p
        elif self.pos.x - offset_p < 0:
            self.pos.x = offset_p
        if self.pos.y > 320:
            self.pos.y = 320
            self.vel.y = 0

        # Update position
        self.rect.midbottom = self.pos