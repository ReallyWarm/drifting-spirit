import pygame, random
from .particle import SplashVFX, DustVFX

class ParticleList():
    def __init__(self):
        self.particle_data = dict()
        self.particle_type = dict()
        self.time = dict()
        self.particles = list()

    def new_type(self, name, type, data, time=1):
        self.particle_data[name] = data
        self.particle_type[name] = type
        self.time[name] = [0, time]

    def get_name(self):
        return [key for key in self.particle_type]
    
    def add(self, name, location, dt):
        tmp = self.particle_data[name]
        thistype = self.particle_type[name]
        self.time[name][0] += 1
        if self.time[name][0] >= self.time[name][1] / dt:
            if thistype == 1:
                self.particles.append(SplashVFX(tmp[0], location, random.randint(tmp[1][0], tmp[1][1]), random.randint(tmp[2][0], tmp[2][1]), 
                                                tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8]))
            if thistype == 2:
                self.particles.append(DustVFX())

            self.time[name][0] = 0

    def update(self, dt):
        for i, particle in reversed(list(enumerate(self.particles))):
            particle.update(dt)
            if not particle.alive:
                self.particles.pop(i)

    def draw(self, surf):
        for particle in self.particles:
            particle.draw(surf)
        