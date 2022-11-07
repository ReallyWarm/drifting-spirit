import pygame, random, math
from engine.graphic.particlelist import ParticleList

class BulletList():
    def __init__(self):
        self.bullets = list()
        self.collide = False
        self.border = None

    def add_border(self, border):
        self.border = border
    
    def add(self, location:list, size:int, speed:float, angle:float, time:int=500,
            force:tuple=None, color:tuple=(255,255,255), particle:bool=False, gravity:bool=False):

        self.bullets.append(Bullet(location, size, speed, angle, time=time, force=force, 
                                   color=color, particle=particle, gravity=gravity))

    def get_colliderect(self):
        temp = self.collide
        self.collide = False
        return temp

    def update(self, dt, collide_rect=None):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(dt)
                if collide_rect is not None:
                    if bullet.rect.colliderect(collide_rect):
                        self.collide = True
                        bullet.alive = False
                if not bullet.alive:
                    self.bullets.remove(bullet)
                if self.border is not None:
                    if bullet.loc[0] > self.border[0] + bullet.spd * bullet.rect.width * 2 or bullet.loc[0] < -bullet.spd * bullet.rect.height * 2:
                        self.bullets.remove(bullet)
                    elif bullet.loc[1] > self.border[1] + bullet.spd * bullet.rect.width * 2 or bullet.loc[1] < -bullet.spd * bullet.rect.height * 2:
                        self.bullets.remove(bullet)
                        
    def draw(self, surf, offset=[0,0]):
        for bullet in self.bullets:
            bullet.draw(surf, offset)

class Bullet():
    def __init__(self, location:list, size:int, speed:float, angle:float, time:int=500,
                 force:tuple=None, color:tuple=(255,255,255), particle:bool=False, gravity:bool=False):
        self.loc = location
        self.rect = pygame.Rect(self.loc[0]-round(size/2), self.loc[1]-round(size/2), size, size)
        self.spd = speed
        self.ang = math.radians(angle)
        self.time = [0,time]
        self.movement = []
        self.force = force
        self.color = color
        self.glow_color = (max(self.color[0]-100,0), max(self.color[1]-100,0), max(self.color[2]-100,0))
        self.gravity = gravity
        self.alive = True

        self.image = self.bullet_sprite()

        self.particle = particle
        self.particles = ParticleList()
        self.particles.new_type('nrm',1,[1,(self.spd//4,self.spd//2),(angle+175,angle+185),self.rect.width//6,0.05,None,self.color,self.glow_color, False])

    def next_movement(self, dt):
        return [self.spd * math.cos(self.ang) * dt, self.spd * math.sin(self.ang) * dt]

    def calculate_force(self, forceX, forceY, dt):
        moveX, moveY = self.movement
        
        if self.gravity:
            moveY += min(forceY * dt, self.spd * dt)
            if forceY >= 0:
                moveX += 0 if moveY >= 0 else (forceX * dt) if moveX >= 0 else -(forceX * dt)
            if forceY < 0:
                moveX -= 0 if moveY <= 0 else (forceX * dt) if moveX >= 0 else -(forceX * dt)
        else:
            moveY += forceY * dt
            moveX += forceX * dt
            
        self.ang = math.atan2(moveY, moveX)

    def update(self, dt):
        self.movement = self.next_movement(dt)
        # self.loc[0] += self.movement[0]
        # self.loc[1] += self.movement[1]
        # self.rect.x = round(self.loc[0])
        # self.rect.y = round(self.loc[1])

        if self.force:
            self.calculate_force(self.force[0], self.force[1], dt)

        if self.particle:
            offset_pos = self.rect.width//6
            self.particles.add('nrm', 
                                [random.randint(self.rect.centerx-offset_pos,self.rect.centerx+offset_pos),
                                 random.randint(self.rect.centery-offset_pos,self.rect.centery+offset_pos)],
                                dt)
        self.particles.update(dt)

        self.time[0] += 1

        if self.time[0] >= self.time[1] / dt:
            self.alive = False

    def bullet_sprite(self):
        surf = pygame.Surface((self.rect.width*2, self.rect.height*2), pygame.SRCALPHA)
        newsurf = surf.copy()
        pygame.draw.circle(surf, self.color, self.rect.size, self.rect.width / 2)
        pygame.draw.circle(newsurf, self.glow_color, self.rect.size, self.rect.width)
        surf.blit(newsurf, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return surf

    def draw(self, surf, offset=[0,0]):
        self.particles.draw(surf, offset)
        if self.alive:
            new_pos = [self.rect.x, self.rect.y]
            new_pos[0] -= offset[0] + self.rect.width / 2
            new_pos[1] -= offset[1] + self.rect.height / 2
            # Circle
            surf.blit(self.image, new_pos, special_flags=pygame.BLEND_RGB_ADD)
                
                