import pygame, math

class SplashVFX():
    def __init__(self, type:int, location:list, speed:float, angle:float, scale:float, 
                 friction:float=0.1, force:tuple=None, color:tuple=(255,255,255), glowColor:tuple=None, gravity:bool=False):
        self.type = type
        self.loc = location
        self.maxspd = speed
        self.spd = speed
        self.ang = math.radians(angle)
        self.scl = scale
        self.fric = friction
        self.movement = []
        self.force = force
        self.color = color
        self.glowColor = glowColor
        self.gravity = gravity
        self.alive = True

    def next_movement(self, dt):
        return [self.spd * math.cos(self.ang) * dt, self.spd * math.sin(self.ang) * dt]

    def calculate_force(self, forceX, forceY, dt):
        moveX, moveY = self.movement
        
        if self.gravity:
            moveY += min(forceY * dt, self.maxspd * dt)
            moveX += 0 if moveY >= 0 else (forceX * dt) if moveX >= 0 else -(forceX * dt)
        else:
            moveY += forceY * dt
            moveX += forceX * dt
            
        self.ang = math.atan2(moveY, moveX)

    def update(self, dt):
        self.movement = self.next_movement(dt)
        self.loc[0] += self.movement[0]
        self.loc[1] += self.movement[1]

        self.spd -= self.fric
        if self.force:
            self.calculate_force(self.force[0], self.force[1], dt)

        if self.spd <= 0:
            self.alive = False

    def circle_glow(self, radius, color):
        newsurf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(newsurf, color, (radius, radius), radius)
        return newsurf

    def draw(self, surf):
        if self.alive:
            # Circle
            if self.type == 1:
                size = self.scl * self.spd / self.maxspd
                pygame.draw.circle(surf, self.color, self.loc, size)

                if self.glowColor:
                    radius = size * 5 / 2
                    surf.blit(self.circle_glow(radius, self.glowColor), (self.loc[0] - radius, self.loc[1] - radius), special_flags=pygame.BLEND_RGB_ADD)
            # Spark shrink
            if self.type == 2:
                points = [
                [self.loc[0] , self.loc[1]],
                [self.loc[0] - self.spd * self.scl * math.cos(self.ang + math.pi/6) * 0.6, self.loc[1] - self.spd * self.scl * math.sin(self.ang + math.pi/6) * 0.6],
                [self.loc[0] - self.spd * self.scl * math.cos(self.ang) * 4, self.loc[1] - self.spd * self.scl * math.sin(self.ang) * 4],
                [self.loc[0] - self.spd * self.scl * math.cos(self.ang - math.pi/6) * 0.6, self.loc[1] - self.spd * self.scl * math.sin(self.ang - math.pi/6) * 0.6]
                ]
                pygame.draw.polygon(surf, self.color, points)
            # Spark shrink side
            if self.type == 3:
                dst_multi = (self.maxspd-self.spd)/self.maxspd
                points = [
                [self.loc[0] , self.loc[1]],
                [self.loc[0] - self.scl * math.cos(self.ang + math.pi/2*dst_multi), self.loc[1] - self.scl * math.sin(self.ang + math.pi/2*dst_multi)],
                [self.loc[0] - self.spd * self.scl * math.cos(self.ang) * 2, self.loc[1] - self.spd * self.scl * math.sin(self.ang) * 2],
                [self.loc[0] - self.scl * math.cos(self.ang - math.pi/2*dst_multi), self.loc[1] - self.scl * math.sin(self.ang - math.pi/2*dst_multi)]
                ]
                pygame.draw.polygon(surf, self.color, points)

class DustVFX():
    def __init__(self, a):
        self.a = a
