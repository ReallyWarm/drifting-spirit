import pygame, random, math
from engine.graphic.spritesheet import sprite_at
from engine.graphic.particlelist import ParticleList

class DangerZone(pygame.sprite.Sprite):
    def __init__(self, pos, canvaSize, offset_player=106):
        self.image = pygame.Surface(canvaSize)
        self.image.fill((23,27,63))
        self.rect = self.image.get_rect(topleft = pos)
        self.offset_player = offset_player
        self.pos = [pos[0],pos[1]+self.offset_player]
        self.top_height = self.pos[1]

        self.clouds = ParticleList()
        self.clouds.new_type('cloud',1,[1,(3,3),(360,360),7,0.015,None,(23,27,63),None,False],5)
        self.clouds.add_border(borderx=(0,self.rect.width))
        self.smokes = ParticleList()
        self.smokes.new_type('smoke',1,[1,(1,3),(250,290),4,0.1,(-0.1,0.5),(11,32,90),None,True],10)

    def update_height(self, player_pos):
        if self.top_height > player_pos[1]:
            self.top_height = player_pos[1]

    def update(self, dt):
        if self.top_height != self.rect[1] - self.offset_player:
            self.pos[1] += ((self.top_height - self.pos[1] + self.offset_player) / 5) * dt 
            self.rect.y = round(self.pos[1])

        self.clouds.add('cloud', [self.rect.left,self.rect.top], dt)
        self.clouds.add('cloud', [self.rect.right,self.rect.top], dt, angle=(180,180))
        self.smokes.add('smoke', [random.randint(self.rect.left+10,self.rect.right-10),self.rect.top], dt)
        self.clouds.update(dt, set_pos=(None,self.rect.y))
        self.smokes.update(dt)
    
    def draw(self, surf, offset=[0,0]):
        self.clouds.draw(surf, offset)
        self.smokes.draw(surf, offset)
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = sprite_at("sprite/portal.png", (0,0,32,48))
        self.rect = self.image.get_rect(topleft = pos)
        self.finish_time = [0, 180]
        self.finished = False

        self.particles = ParticleList()
        self.particles.new_type('light',1,[1,(1,2),(250,290),2,0.05,None,(192,245,255),(20,20,20),False],20)
        self.particles.new_type('finish',1,[1,(4,5),(0,360),5,0.1,None,(192,245,255),(20,20,20),False],0)
        self.particle_color = ((192,245,255),(255,220,192))

    def update(self, dt):
        self.particles.add('light', [random.randint(self.rect.left,self.rect.right),self.rect.bottom], dt, color=self.particle_color[random.randrange(0,2)])
        self.particles.update(dt)

    def finish_effect(self, dt, surf_size):
        if not self.finished:
            w = surf_size[0] // 2
            h = surf_size[1] // 2
            fh = (h*4)//3
            for _ in range(4):
                side = random.randint(1,4)
                if side == 1:
                    pos = [self.rect.centerx-w, random.randint(self.rect.centery-fh,self.rect.centery+h)]
                elif side == 2:
                    pos = [self.rect.centerx+w, random.randint(self.rect.centery-fh,self.rect.centery+h)]
                elif side == 3:
                    pos = [random.randint(self.rect.centerx-w,self.rect.centerx+w), self.rect.centery-fh]
                elif side == 4:
                    pos = [random.randint(self.rect.centerx-w,self.rect.centerx+w), self.rect.centery+h]
                angle = round(math.degrees(math.atan2(self.rect.centery-pos[1],self.rect.centerx-pos[0])))

                self.particles.add('finish', pos, dt, color=self.particle_color[random.randrange(0,2)], angle=(angle,angle))

            self.particles.update(dt)
            self.finish_time[0] += 1

            if self.finish_time[0] >= self.finish_time[1] / dt:
                self.finished = True
                self.finish_time[0] = 0

    
    def draw(self, surf, offset=[0,0]):
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))
        self.particles.draw(surf, offset)