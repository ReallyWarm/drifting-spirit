import pygame
from engine.graphic.spritesheet import sprite_at

class DangerZone(pygame.sprite.Sprite):
    def __init__(self, pos, canvaSize, offset_player=106):
        self.image = pygame.Surface(canvaSize)
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.offset_player = offset_player
        self.pos = [pos[0],pos[1]+self.offset_player]
        self.top_height = self.pos[1]

    def update_height(self, player_pos):
        if self.top_height > player_pos[1]:
            self.top_height = player_pos[1]

    def update(self, dt):
        if self.top_height != self.rect[1] - self.offset_player:
            self.pos[1] += ((self.top_height - self.pos[1] + self.offset_player) / 5) * dt 
            self.rect[1] = round(self.pos[1])
    
    def draw(self, surf, offset=[0,0]):
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = sprite_at("sprite/heart-ui.png", (0,0,32,48))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, dt):
        pass
    
    def draw(self, surf, offset=[0,0]):
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))