import pygame, random
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

    def update(self, dt):
        pass
    
    def draw(self, surf, offset=[0,0]):
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))