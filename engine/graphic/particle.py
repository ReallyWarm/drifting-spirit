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
        self.loc[0] += self.movement[0]
        self.loc[1] += self.movement[1]

        self.spd -= self.fric * dt
        if self.force:
            self.calculate_force(self.force[0], self.force[1], dt)

        if self.spd <= 0:
            self.alive = False

    def circle_glow(self, radius, color):
        newsurf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(newsurf, color, (radius, radius), radius)
        return newsurf

    def draw(self, surf, offset=[0,0]):
        if self.alive:
            new_pos = self.loc.copy()
            new_pos[0] -= offset[0]
            new_pos[1] -= offset[1]
            # Circle
            if self.type == 1:
                size = self.scl * self.spd / self.maxspd
                pygame.draw.circle(surf, self.color, new_pos, size)

                if self.glowColor:
                    radius = size * 5 / 2
                    surf.blit(self.circle_glow(radius, self.glowColor), (new_pos[0] - radius, new_pos[1] - radius), special_flags=pygame.BLEND_RGB_ADD)
            # Spark shrink
            if self.type == 2:
                points = [
                [new_pos[0] , new_pos[1]],
                [new_pos[0] - self.spd * self.scl * math.cos(self.ang + math.pi/6) * 0.6, new_pos[1] - self.spd * self.scl * math.sin(self.ang + math.pi/6) * 0.6],
                [new_pos[0] - self.spd * self.scl * math.cos(self.ang) * 4, new_pos[1] - self.spd * self.scl * math.sin(self.ang) * 4],
                [new_pos[0] - self.spd * self.scl * math.cos(self.ang - math.pi/6) * 0.6, new_pos[1] - self.spd * self.scl * math.sin(self.ang - math.pi/6) * 0.6]
                ]
                pygame.draw.polygon(surf, self.color, points)
            # Spark shrink side
            if self.type == 3:
                dst_multi = (self.maxspd-self.spd)/self.maxspd
                points = [
                [new_pos[0] , new_pos[1]],
                [new_pos[0] - self.scl * math.cos(self.ang + math.pi/2*dst_multi), new_pos[1] - self.scl * math.sin(self.ang + math.pi/2*dst_multi)],
                [new_pos[0] - self.spd * self.scl * math.cos(self.ang) * 2, new_pos[1] - self.spd * self.scl * math.sin(self.ang) * 2],
                [new_pos[0] - self.scl * math.cos(self.ang - math.pi/2*dst_multi), new_pos[1] - self.scl * math.sin(self.ang - math.pi/2*dst_multi)]
                ]
                pygame.draw.polygon(surf, self.color, points)

class MaskVFX():
    def __init__(self, image:pygame.Surface, location:list, speed:float, angle:float, scale:float, time:int, color:tuple=(255,255,255), alpha_multi=1):
        self.end_alpha = 255 / time
        self.time = time
        self.loc = location
        self.spd = speed
        self.ang = math.radians(angle)
        self.alpha_multi = alpha_multi
        self.mask_surf = pygame.mask.from_surface(image)
        self.mask = self.mask_surf.to_surface(unsetcolor=(0,0,0,0), setcolor=(color[0],color[1],color[2],self.end_alpha*self.time*self.alpha_multi))
        if scale != 1:
            self.scl = scale
            self.mask = pygame.transform.scale(self.mask, (self.mask.get_width()*scale, self.mask.get_height()*scale))
        self.alive = True
    
    def next_movement(self, dt):
        return [self.spd * math.cos(self.ang) * dt, self.spd * math.sin(self.ang) * dt]

    def update(self, dt):
        movement = self.next_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        self.mask.set_alpha(self.end_alpha*self.time*self.alpha_multi)

        self.time -= 1 * dt
        if self.time <= 0:
            self.alive = False

    def draw(self, surf, offset=[0,0]):
        if self.alive:
            new_pos = self.loc.copy()
            new_pos[0] -= offset[0]
            new_pos[1] -= offset[1]
            surf.blit(self.mask, new_pos)