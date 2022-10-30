import pygame
from engine.graphic.animate import Animate

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.left+2, self.rect.top+2, self.rect.width-4, self.rect.height-4)

class Ghost(Enemy):
    def __init__(self, pos):
        # Animation and Image
        self.ani = {'idle': Animate("sprite/ghost-idle.png",(0,0,32,32), 4, pixel_jump=2, frames=25)}
        self.state = 'idle'

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image)

    def update(self, dt):
        self.image = self.ani[self.state].update(dt)

class Imp(Enemy):
    def __init__(self, pos):
        # Animation and Image
        self.ani = {'idle': Animate("sprite/imp-idle.png",(0,0,32,32), 9, pixel_jump=2, frames=25)}
        self.state = 'idle'

        if pos[0] < 128:
            for name in self.ani:
                for i, image in enumerate(self.ani[name].sprites):
                    self.ani[name].sprites[i] = pygame.transform.flip(image, True, False)

        super().__init__(pos, self.ani['idle'].image)
    
    def update(self, dt):
        self.image = self.ani[self.state].update(dt)

class DangerZone(Enemy):
    def __init__(self, pos, canvaSize, offset_player=106):
        image = pygame.Surface(canvaSize)
        image.fill((0,0,0))
        self.offset_player = offset_player
        self.pos = [pos[0],pos[1]+self.offset_player]
        self.top_height = self.pos[1]

        super().__init__(self.pos, image)

    def update_height(self, player_pos):
        if self.top_height > player_pos[1]:
            self.top_height = player_pos[1]

    def update(self, dt):
        if self.top_height != self.pos[1]:
            self.pos[1] += ((self.top_height - self.pos[1] + self.offset_player) / 5) * dt 
            self.rect[1] = self.pos[1]
    
    def draw(self, surf, offset):
        surf.blit(self.image, (self.rect.x-offset[0], self.rect.y-offset[1]))