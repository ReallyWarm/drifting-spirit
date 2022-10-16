from platform import platform
import pygame, sys
from engine.graphic.spritesheet import load_sheet
from engine.graphic.particlelist import ParticleList
from engine.platform import PlatformSet, Platform
from engine.player import Player

class Game():
    def __init__(self, canva_size):
        self.canva = pygame.Surface(canva_size) # 3:2
        self.cva_rect = self.canva.get_rect()
        self.scale = (1,1)
        self.update_canva()

        plat_image = list()
        plat_image.extend(load_sheet("sprite/platform.png", (0,0,32,16), 4))
        plat_image.extend(load_sheet("sprite/platform.png", (0,16,32,16), 4))
        self.plat_data = PlatformSet()
        self.plat_data.add('n1b', [plat_image[3]])
        self.plat_data.add('n2b', [plat_image[0],plat_image[2]])
        self.plat_data.add('n3b', [plat_image[0],plat_image[1],plat_image[2]])

        self.particles = ParticleList()
        self.particles.new_type('flame0',1,[1,(1,2),(250,290), 4, 0.05,(-1,-0.1),(255,120, 60), (55,25,15), True])
        self.particles.new_type('candle',1,[1,(1,2),(250,290), 4, 0.2, (0,-15),(204,255,255), (0,20,20), False], 0)
        self.particles.new_type('spark0',1,[2,(3,4),(  0,360), 2, 0.05,     None,(200,200,100), False, False])
        self.particles.new_type('dusts0',1,[1,(2,3),(180,360), 4, 0.1 ,(0.1,0.1),(255,255,255), False, True])
        self.particles.add_border(canva_size)
        self.ptc_id = 'flame0'

        self.player_sprites = pygame.sprite.GroupSingle()
        self.block_sprites = pygame.sprite.Group()
        self.plat_sprites = pygame.sprite.Group()

        self.offset = [0,0]
        self.dt = 1

    def init_level(self):
        self.player_sprites.empty()
        self.player = Player()
        self.player_sprites.add(self.player)

        self.plat_sprites.empty()
        for i in range (5):
            plat = Platform((100,32+64*i), self.plat_data.data['n3b'])
            self.plat_sprites.add(plat)

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

    def update(self, event_list, dt):
        self.dt = dt
        self.input(event_list)
        self.player.input(event_list)
        self.player.move(self.block_sprites.sprites(), self.plat_sprites.sprites(), dt)
        self.particles.update(self.dt)
        self.plat_sprites.update(self.dt)
        self.player.update(self.dt)
        self.scroll(self.dt)

    def draw(self):
        self.canva.fill((0,0,100))

        self.particles.draw(self.canva)
        for i in range(7):
            pygame.draw.rect(self.canva, (200,155,155),pygame.Rect(32*i,100,32,32+i*10))
        for i in range(10):
            pygame.draw.rect(self.canva, (25*i,255,255//(i+1)),pygame.Rect(224,32*i,32,32))

        for platform in self.plat_sprites:
            self.canva.blit(platform.image, (platform.rect.x-self.offset[0], platform.rect.y-self.offset[1]))

        self.canva.blit(self.player.image, (self.player.rect.x-self.offset[0], self.player.rect.y-self.offset[1]))
        self.player.vfx.draw(self.canva, self.offset)

        self.screen.blit(pygame.transform.scale(self.canva, self.cva_rect.size), self.cva_rect.topleft)

    def scroll(self, dt):
        # Lock player
        # self.offset[0] += (self.player.rect.centerx - self.offset[0] - (self.canva.get_width()/2)) / 5 # offset X
        # self.offset[1] += (self.player.rect.centery - self.offset[1] - (self.canva.get_height()/2)) / 5 # offset Y

        # Lock offset player
        # self.offset[0] += (self.player.rect.centerx - self.offset[0] - (self.canva.get_width()/2)) / 5 # offset X
        self.offset[1] += (self.player.rect.centery - self.offset[1] - (self.canva.get_height()*6/7)) / 5 # offset Y

        # self.offset = [0,0]
        # player_y = self.player.rect.bottom
        # hit_plat = self.player.vel.y
        # if player_y < 192:
        #     if hit_plat == 0:
        #         self.offset[1] = 2
        # else:
        #     self.offset[1] = 0
