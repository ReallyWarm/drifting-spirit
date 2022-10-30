import pygame
from pygame.math import Vector2
from engine.graphic.animate import Animate
from engine.graphic.particlelist import ParticleList

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Animation and Image
        self.ani = {'run' : Animate("sprite/player-run.png", (0,0,24,32), 8, pixel_jump=2, frames=3),
                    'idle': Animate("sprite/player-idle.png",(0,0,24,32), 4, pixel_jump=2, frames=45),
                    'fall': Animate("sprite/player-fall.png",(0,0,24,32), 1),
                    'jump': Animate("sprite/player-jump.png",(0,0,24,32), 1),
                    'dshX': Animate("sprite/player-dashes.png",(0,0,24,32), 1),
                    'dshD': Animate("sprite/player-dashes.png",(2,0,24,32), 1, start_at=1),
                    'dshU': Animate("sprite/player-dashes.png",(2,0,24,32), 1, start_at=2)}
        self.image = self.ani['idle'].image
        self.rect = self.image.get_rect(midbottom = pos)

        # VFX
        self.vfx_top = ParticleList()
        self.vfx_top.new_type('candle',1,[1,(1,2),(245,295), 5, 0.2, (0,-1.5),(204,255,255), (0,20,20), False])
        self.vfx_back = ParticleList()
        self.vfx_back.new_type('maskDXR',3,[self.ani['dshX'].image, 0, 90, 1, 10, (204,255,255)])
        self.vfx_back.new_type('maskDXL',3,[pygame.transform.flip(self.ani['dshX'].image, True, False), 0, 90, 1, 10, (204,255,255)])
        self.vfx_back.new_type('maskDD',3,[self.ani['dshD'].image, 0, 90, 1, 10, (204,255,255)])
        self.vfx_back.new_type('maskDU',3,[self.ani['dshU'].image, 0, 90, 1, 10, (204,255,255)])
        self.mask_color_extra = (255,240,204)

        self.state = 'idel'
        self.face_right = True
        self.hit_ground = False

        self.moveL = False
        self.moveR = False
        self.moveU = False
        self.moveD = False

        self.jump_time = [0,12]
        self.jumped = False
        self.jumping = False

        self.max_health = 5
        self.health = self.max_health
        self.rg_health = 0

        self.power_default = 2
        self.power_amount = self.power_default
        self.recharge_time = [0,100]

        self.dashing = False
        self.dash_direct = 0
        self.dash_time = [0,14]

        self.damaged = False
        self.immunity = False
        self.immunity_time = [0,45]
        
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
                    if self.health + self.rg_health < self.max_health:
                        self.rg_health += 1
                    self.moveU = True
                if event.key == pygame.K_s:
                    self.moveD = True
                if event.key == pygame.K_j:
                    self.power_amount = 6
                    if not self.jumping:
                        self.jumped = True
                if event.key == pygame.K_k:
                    if self.power_amount > 0 and not self.dashing:
                        self.power_amount -= 1
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
        if self.face_right or self.state == 'dshD' or self.state == 'dshU':
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # Player VFX
        mid_x, top_y = self.rect.midtop
        if self.state == 'idle' and self.ani['idle'].image_num != 3:
            top_y += 2
        
        for i in range(2):
            self.vfx_top.add('candle', [mid_x, top_y], dt)
        self.vfx_top.update(dt)

        if self.dashing:
            dash_key = ''
            if self.state == 'dshX':
                dash_key = 'maskDXR' if self.face_right else 'maskDXL'
            elif self.state == 'dshD':
                dash_key = 'maskDD'
            elif self.state == 'dshU':
                dash_key = 'maskDU'
            
            dash_color = None
            if self.power_amount >= self.power_default:
                dash_color = self.mask_color_extra
            self.vfx_back.add(dash_key, [self.rect.x, self.rect.y], dt, alpha_multi=0.5,color=dash_color)

        self.vfx_back.update(dt)

        # Power recharge
        if self.power_amount < self.power_default:
            if self.recharge_time[0] < self.recharge_time[1] / dt:
                self.recharge_time[0] += 1
            else:
                self.power_amount += 1
                self.recharge_time[0] = 0

        if self.damaged:
            if self.rg_health == 0:
                self.health -= 1 
            else:
                self.rg_health -= 1

            self.immunity = True
            self.damaged = False

        # Immunity effect
        if self.immunity and self.immunity_time[0] < self.immunity_time[1] / dt:
            fade = self.image.copy()
            if self.immunity_time[0] % 10 >= 5:
                fade.set_alpha(200)
            else:
                fade.set_alpha(100)
            self.image = fade
            self.immunity_time[0] += 1
        else:
            self.immunity = False
            self.immunity_time[0] = 0


    def move(self, collision_block, collision_platform, dt):
        # Max speed = acc / fric
        acc = 0.5
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
        self.hit_ground = False
        hit_y = False

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
        if not self.moveD and self.vel.y > 0:
            for platform in collision_platform:
                if platform.rect.colliderect(new_rect):
                    if self.rect.bottom <= platform.rect.top < new_rect.bottom:
                        new_rect.bottom = platform.rect.top
                        hit_y = True
        # collide block Y
        for block in collision_block:
            if block.rect.colliderect(new_rect):
                if self.vel.y > 0:
                    new_rect.bottom = block.rect.top
                elif self.vel.y < 0:
                    new_rect.top = block.rect.bottom
                hit_y = True

        # Collide map
        if new_rect.right > 256:
            new_rect.right = 256
        elif new_rect.left < 0:
            new_rect.left = 0
        if new_rect.bottom > 320:
            new_rect.bottom = 320
            hit_y = True

        # If hit Y
        if hit_y:
            self.vel.y = 0
            self.jumping = False
            self.hit_ground = True

        self.pos = new_rect.topleft

        return new_rect