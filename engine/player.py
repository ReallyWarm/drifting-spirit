import pygame
from pygame.math import Vector2
from engine.graphic.animate import Animate
from engine.graphic.particlelist import ParticleList

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ani = {'run' : Animate("sprite/player-run.png", (0,0,24,32), 8, pixel_jump=2, frames=3),
                    'idle': Animate("sprite/player-idle.png",(0,0,24,32), 4, pixel_jump=2, frames=45),
                    'fall': Animate("sprite/player-fall.png",(0,0,24,32), 1),
                    'jump': Animate("sprite/player-jump.png",(0,0,24,32), 1),
                    'dshX': Animate("sprite/player-dashes.png",(0,0,24,32), 1),
                    'dshD': Animate("sprite/player-dashes.png",(2,0,24,32), 1, start_at=1),
                    'dshU': Animate("sprite/player-dashes.png",(2,0,24,32), 1, start_at=2)}
        self.image = self.ani['idle'].image
        self.rect = self.image.get_rect(midbottom = (150,300))

        self.vfx = ParticleList()
        self.vfx.new_type('candle',1,[1,(1,2),(245,295), 5, 0.2, (0,-1.5),(204,255,255), (0,20,20), False], 0)

        self.state = 'idel'
        self.face_right = True
        self.moveL = False
        self.moveR = False
        self.moveU = False
        self.moveD = False
        self.jump_time = [0,15]
        self.jumped = False
        self.jumping = False
        self.dashing = False
        self.dash_direct = 0
        self.dash_time = [0,16]
        
        self.pos = Vector2(self.rect.topleft)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.moveL = True
                if event.key == pygame.K_d:
                    self.moveR = True
                if event.key == pygame.K_w:
                    self.moveU = True
                if event.key == pygame.K_s:
                    self.moveD = True
                if event.key == pygame.K_j:
                    if not self.jumping:
                        self.jumped = True
                if event.key == pygame.K_k:
                    self.dashing = True
                    if self.moveU:
                        self.dash_direct = 1
                    elif self.moveD:
                        self.dash_direct = 2
                    elif self.face_right:
                        self.dash_direct = 3
                    else:
                        self.dash_direct = 4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.moveL = False
                if event.key == pygame.K_d:
                    self.moveR = False
                if event.key == pygame.K_w:
                    self.moveU = False
                if event.key == pygame.K_s:
                    self.moveD = False
                if event.key == pygame.K_j:
                    self.jumped = False

    def update(self, dt):
        print(self.dash_direct)
        if self.dash_direct == 1:
            self.state = 'dshU'
        elif self.dash_direct == 2:
            self.state = 'dshD'
        elif self.dashing:
            self.state = 'dshX'
        elif self.vel.y > 1:
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

    def move(self, collision_block, collision_platform, dt):
        # Max speed = acc / fric
        acc = 0.6
        fric = -0.15
        max_y = 6
        self.acc = Vector2(0, 0.2*dt)

        # Direction
        if self.moveR and self.moveL:
            direction_x = 0
        elif self.moveR:
            self.face_right = True
            direction_x = 1
        elif self.moveL:
            self.face_right = False
            direction_x = -1
        else:
            direction_x = 0

        # Dashing take priority
        if self.dashing:
            if self.dash_time[0] < self.dash_time[1] / dt:
                self.vel = Vector2(0,0)
                self.dash_time[0] += 1
                dash_x = 4 * dt
                dash_y = 5 * dt

                if self.dash_direct == 1:
                    self.vel.y = -dash_y
                elif self.dash_direct == 2:
                    self.vel.y = dash_y
                elif self.dash_direct == 3:
                    self.vel.x = dash_x
                elif self.dash_direct == 4:
                    self.vel.x = -dash_x
            else:
                self.dashing = False
                self.dash_direct = 0
                self.dash_time[0] = 0
                self.vel /= 4

        # Jump and Run
        else:
            # Jumping
            if self.jumped and self.jump_time[0] < self.jump_time[1] / dt:
                self.vel.y = -3.6 * dt
                self.jump_time[0] += 1
                self.jumping = True
            else:
                self.jumped = False
                self.jump_time[0] = 0

            # Running    
            self.acc.x = direction_x * acc * dt
            self.acc.x += self.vel.x * fric

            # Update velocity
            self.vel += self.acc * dt
            if self.vel.y > max_y * dt:
                self.vel.y = max_y * dt

        self.pos += self.vel + (0.5 * self.acc)

        # Stopping
        if self.vel.x < 0.08 * dt and self.vel.x > -0.08 * dt:
            self.vel.x = 0

        # Update position
        self.rect = self.collision(collision_block, collision_platform)

    def collision(self, collision_block, collision_platform):
        new_rect = self.rect.copy()

        new_rect.x = round(self.pos.x)
        # collide block X
        for block in collision_block:
            if block.rect.colliderect(new_rect):
                if self.vel.x > 0:
                    new_rect.right = block.rect.left
                elif self.vel.x < 0:
                    new_rect.left = block.rect.right

        new_rect.y = round(self.pos.y)
        # collide platform
        if not self.moveD:
            for platform in collision_platform:
                if platform.rect.colliderect(new_rect):
                    if self.vel.y > 0:
                        if abs(new_rect.bottom - platform.rect.top) <= platform.rect.height//2:
                            new_rect.bottom = platform.rect.top
                            self.vel.y = 0
                            self.jumping = False
        # collide block Y
        for block in collision_block:
            if block.rect.colliderect(new_rect):
                if self.vel.y > 0:
                    new_rect.bottom = block.rect.top
                elif self.vel.y < 0:
                    new_rect.top = block.rect.bottom
                self.vel.y = 0
                self.jumping = False

        # Collide map
        if new_rect.right > 256:
            new_rect.right = 256
        elif new_rect.left < 0:
            new_rect.left = 0
        if new_rect.bottom > 320:
            new_rect.bottom = 320
            self.vel.y = 0
            self.jumping = False

        self.pos = new_rect.topleft

        return new_rect