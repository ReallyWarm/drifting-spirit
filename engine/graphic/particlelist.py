import pygame, random
from .particle import SplashVFX, DustVFX, MaskVFX

class ParticleList():
    def __init__(self):
        self.particle_data = dict()
        self.particle_type = dict()
        self.time = dict()
        self.particles = list()
        self.border = None

    def new_type(self, name, type, data, time=1):
        self.particle_data[name] = data
        self.particle_type[name] = type
        self.time[name] = [0, time]

    def get_name(self):
        return [key for key in self.particle_type]

    def add_border(self, border):
        self.border = border
    
    def add(self, name, location, dt, 
                  angle:list=None, fric=None, # type 1
                  alpha_multi=1, color=None): # type 3
        tmp = self.particle_data[name].copy()

        if angle is not None:
            tmp[2] = angle
        
        thistype = self.particle_type[name]
        self.time[name][0] += 1
        if self.time[name][0] >= self.time[name][1] / dt:
            if thistype == 1:
                if fric is not None:
                    tmp[4] = fric
                if color is not None:
                    tmp[6] = color
                self.particles.append(SplashVFX(tmp[0], location, random.randint(tmp[1][0], tmp[1][1]), random.randint(tmp[2][0], tmp[2][1]), 
                                                tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8]))
            if thistype == 2:
                self.particles.append(DustVFX())
            if thistype == 3:
                if color is not None:
                    tmp[5] = color
                self.particles.append(MaskVFX(tmp[0], location, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], alpha_multi))

            self.time[name][0] = 0

    def update(self, dt):
        for i, particle in reversed(list(enumerate(self.particles))):
            particle.update(dt)
            if not particle.alive:
                self.particles.pop(i)
            if self.border is not None:
                if particle.loc[0] > self.border[0] + particle.spd * particle.scl * 4 or particle.loc[0] < -particle.spd * particle.scl * 4:
                    self.particles.pop(i)
                elif particle.loc[1] > self.border[1] + particle.spd * particle.scl * 4 or particle.loc[1] < -particle.spd * particle.scl * 4:
                    self.particles.pop(i)
    def draw(self, surf, offset=[0,0]):
        for particle in self.particles:
            particle.draw(surf, offset)
        