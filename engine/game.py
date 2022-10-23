import pygame
from engine.graphic.spritesheet import load_sheet
from engine.graphic.gameui import PowerUI
from engine.graphic.particlelist import ParticleList
from engine.platform import PlatformSet, Platform
from engine.enemy import ImpEnemy
from engine.player import Player
from engine.genlevel import gen_level

class Game():
    def __init__(self, canva_size):
        self.screen = pygame.display.get_surface()
        self.scr_size = pygame.display.get_window_size()
        self.canva = pygame.Surface(canva_size) # 3:2
        self.cva_rect = self.canva.get_rect()
        self.cva_scale = (1,1)
        self.win_scale = (1,1)

        self.normal_power = load_sheet("sprite/platform.png", (0,0,32,32), 2)
        self.extra_power = load_sheet("sprite/player-fall.png", (24,0,32,32), 1)
        self.power_rect = pygame.Rect(40, self.scr_size[1] - 106, 64, 64)
        self.power_offset = (0,76)

        self.update_surface(self.win_scale)

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
        self.enemy_sprites = pygame.sprite.Group()
        self.power_ui_sprites = pygame.sprite.Group()

        self.offset = [0,0]
        self.dt = 1

    def update_surface(self, win_scale):
        self.screen = pygame.display.get_surface()
        self.scr_size = pygame.display.get_window_size()

        cva_w = (((self.scr_size[0] // 15) * 8) // 128) * 128
        cva_h = (cva_w // 4) * 5
        self.cva_rect.size = (cva_w, cva_h)
        self.cva_rect.topleft = ((self.scr_size[0] - cva_w) // 2, (self.scr_size[1] - cva_h) // 2)

        self.cva_scale = (self.canva.get_width() / cva_w, self.canva.get_height() / cva_h)
        self.win_scale = win_scale
        
        sw, sh = self.win_scale
        self.power_rect.size = (64*sw, 64*sh)
        self.power_rect.topleft = (40*sw, self.scr_size[1] - 106*sh)
        self.power_offset = (0*sw, 76*sh)

    def init_level(self):
        self.player_sprites.empty()
        self.player = Player()
        self.player_sprites.add(self.player)

        # Load level data
        self.level = list()
        level_data = gen_level('data/map.json')
        for layer in level_data:
            layer_data = list()
            for data in layer:
                if data[0] in ['n1b','n2b','n3b']:
                    plat = Platform((data[2],self.canva.get_height()-data[3]), self.plat_data.data[data[0]])
                    layer_data.append(plat)
                elif data[0] in ['imp']:
                    enemy = ImpEnemy((data[2],self.canva.get_height()-data[3]))
                    layer_data.append(enemy)
            self.level.append(layer_data)

        # Create on screen level  
        self.plat_sprites.empty()
        self.enemy_sprites.empty()
        self.next_plat = len(self.level) - 1
        for i in range(5):
            self.make_layer(self.level[self.next_plat])
            self.next_plat -= 1

        # init UI
        self.power_ui_sprites.empty()
        self.power_index = 0
        for i in range(self.player.power_default):
            rect = self.power_rect.copy()
            rect.top -= self.power_offset[1] * i
            self.power_index += 1
            self.power_ui_sprites.add(PowerUI(1, self.power_index, rect, self.normal_power))
        
    
    def make_layer(self, layer):
        for data in layer:
            if isinstance(data, Platform):
                self.plat_sprites.add(data)
            elif isinstance(data, ImpEnemy):
                self.enemy_sprites.add(data)

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
                    self.particles.add(self.ptc_id, [(mx-self.cva_rect.x)*self.cva_scale[0], (my-self.cva_rect.y)*self.cva_scale[1]], self.dt)

    def update(self, event_list, dt):
        self.dt = dt
        self.input(event_list)
        self.player.input(event_list)
        self.player.move(self.block_sprites.sprites(), self.plat_sprites.sprites(), dt)
        self.plat_sprites.update(self.dt)
        self.enemy_sprites.update(self.dt)
        self.player.update(self.dt)
        self.particles.update(self.dt)
        self.scroll(self.dt)

        # for i in self.power_ui_sprites.sprites():
        #     print(i.pos, end=" ")
        # print(self.player.power_amount)

        # update UI
        self.power_ui_sprites.update(self.player)
        # Add extra power UI
        for i in range(self.power_index, self.player.power_amount):
            rect = self.power_rect.copy()
            rect.top -= self.power_offset[1] * i
            self.power_index += 1
            self.power_ui_sprites.add(PowerUI(2, self.power_index, rect, self.extra_power))
        # Remove extra power UI
        for power_ui in self.power_ui_sprites.sprites():
            if power_ui.type == 2 and not power_ui.recharge:
                self.power_ui_sprites.remove(power_ui)
                self.power_index -= 1

        print(len(self.enemy_sprites.sprites()))

        # collide enemies
        for enemy in self.enemy_sprites.sprites():
            if enemy.rect.colliderect(self.player.rect):
                if self.player.dashing:
                    self.enemy_sprites.remove(enemy)
                elif not self.player.immunity:
                    if self.player.vel.y > 0:
                        if self.player.rect.bottom <= enemy.rect.centery or self.player.vel.y > enemy.rect.height // 2:
                            self.enemy_sprites.remove(enemy)
                    else:
                        self.player.damaged = True
                        print("hit")

        # Level loading
        top_plat = 320
        # Remove off screen platforms
        for platform in self.plat_sprites.sprites():
            if self.player.rect.bottom - platform.rect.top < -64 and self.player.hit_ground: # 32 * 3/2 + 16
                self.plat_sprites.remove(platform)
            if platform.rect.bottom < top_plat:
                top_plat = platform.rect.bottom
        # Remove off screen enemies
        for enemy in self.enemy_sprites.sprites():
            if self.player.rect.bottom - enemy.rect.top < -64 and self.player.hit_ground: # 32 * 3/2 + 16
                self.enemy_sprites.remove(enemy)      
        # Make next layer
        if top_plat - self.player.rect.top > - 160: # 32 * 3/2 * 3 + 16
            self.make_layer(self.level[self.next_plat])
            if self.next_plat > 0:
                self.next_plat -= 1

    def draw(self):
        self.canva.fill((0,0,100))

        for i in range(7):
            pygame.draw.rect(self.canva, (200,155,155),pygame.Rect(32*i,100,32,32+i*10))
        for i in range(10):
            pygame.draw.rect(self.canva, (25*i,255,255//(i+1)),pygame.Rect(224,32*i,32,32))

        for platform in self.plat_sprites:
            self.canva.blit(platform.image, (platform.rect.x-self.offset[0], platform.rect.y-self.offset[1]))
        for enemy in self.enemy_sprites:
            self.canva.blit(enemy.image, (enemy.rect.x-self.offset[0], enemy.rect.y-self.offset[1]))

        self.player.vfx_back.draw(self.canva, self.offset)
        self.canva.blit(self.player.image, (self.player.rect.x-self.offset[0], self.player.rect.y-self.offset[1]))
        self.player.vfx_top.draw(self.canva, self.offset)

        self.particles.draw(self.canva)

        self.screen.blit(pygame.transform.scale(self.canva, self.cva_rect.size), self.cva_rect.topleft)
        self.power_ui_sprites.draw(self.screen)

    def scroll(self, dt):
        # Lock player
        # self.offset[0] += (self.player.rect.centerx - self.offset[0] - (self.canva.get_width()/2)) / 5 # offset X
        # self.offset[1] += (self.player.rect.centery - self.offset[1] - (self.canva.get_height()/2)) / 5 # offset Y

        # Lock offset player
        # self.offset[0] += (self.player.rect.centerx - self.offset[0] - (self.canva.get_width()/2)) / 5 # offset X
        self.offset[1] += ((self.player.rect.centery - self.offset[1] - (self.canva.get_height()*5/7)) / 5) * dt # offset Y

        # self.offset = [0,0]
        # player_y = self.player.rect.bottom
        # hit_plat = self.player.vel.y
        # if player_y < 192:
        #     if hit_plat == 0:
        #         self.offset[1] = 2
        # else:
        #     self.offset[1] = 0
