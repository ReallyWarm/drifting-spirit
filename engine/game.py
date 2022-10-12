import pygame, sys
from engine.graphic.particlelist import ParticleList
from engine.player import Player

class Game():
    def __init__(self, canvaSize):
        self.canva = pygame.Surface(canvaSize) # 3:2
        self.cva_rect = self.canva.get_rect()
        self.scale = (1,1)
        self.update_canva()

        self.player = Player()
        self.particles = ParticleList()
        self.particles.new_type('flame0',1,[1,(1,2),(250,290), 4, 0.05,(-1,-0.1),(255,120, 60), (55,25,15), True])
        self.particles.new_type('candle',1,[1,(1,2),(250,290), 4, 0.2, (0,-15),(204,255,255), (0,20,20), False], 0)
        self.particles.new_type('spark0',1,[2,(3,4),(  0,360), 2, 0.05,     None,(200,200,100), False, False])
        self.particles.new_type('dusts0',1,[1,(2,3),(180,360), 4, 0.1 ,(0.1,0.1),(255,255,255), False, True])
        self.ptc_id = 'flame0'

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.dt = 1

    def update_canva(self):
        self.screen = pygame.display.get_surface()
        self.scr_size = pygame.display.get_window_size()

        cva_w = (((self.scr_size[0] // 15) * 8) // 128) * 128
        cva_h = (cva_w // 4) * 5
        self.cva_rect.size = (cva_w, cva_h)
        self.cva_rect.topleft = ((self.scr_size[0] - cva_w) // 2, (self.scr_size[1] - cva_h) // 2)
        self.scale = (self.canva.get_width() / cva_w, self.canva.get_height() / cva_h)

    def input(self, event_list):
        mx, my = pygame.mouse.get_pos()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.ptc_id = 'flame0'
                if event.key == pygame.K_w:
                    self.ptc_id = 'spark0'
                if event.key == pygame.K_e:
                    self.ptc_id = 'dusts0'
                if event.key == pygame.K_r:
                    self.ptc_id = 'candle'

            
        if self.cva_rect.collidepoint(mx, my):
            if pygame.mouse.get_pressed()[0]:
                for i in range(1):
                    self.particles.add(self.ptc_id, [(mx-self.cva_rect.x)*self.scale[0], (my-self.cva_rect.y)*self.scale[1]], self.dt)
            if pygame.mouse.get_pressed()[2]:
                self.player.aniType = 'idle'

    def update(self, event_list, dt):
        self.dt = dt
        self.input(event_list)
        self.particles.update(self.dt)
        self.all_sprites.update(self.dt)

    def draw(self):
        rect1 = pygame.Rect(self.canva.get_width()-50,50,50,50)

        self.canva.fill((0,0,100))
        pygame.draw.rect(self.canva, (100,0,0), rect1)
        self.particles.draw(self.canva)
        for i in range(8):
            pygame.draw.rect(self.canva, (200,155,155),pygame.Rect(32*i,100,32,32+i*10))

        self.all_sprites.draw(self.canva)

        self.screen.blit(pygame.transform.scale(self.canva, self.cva_rect.size), self.cva_rect.topleft)