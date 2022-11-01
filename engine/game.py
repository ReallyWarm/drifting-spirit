import pygame
from engine.graphic.spritesheet import sprite_at, load_sheet
from engine.graphic.gameui import HealthUI, PowerUI
from engine.graphic.particlelist import ParticleList
from engine.platform import PlatformSet, Platform
from engine.enemy import Ghost, Imp
from engine.item import ItemDash, ItemHealth, ItemScore
from engine.player import Player
from engine.object import DangerZone, Portal
from engine.genlevel import gen_level

class Game():
    def __init__(self, canva_size, scale):
        self.canva = pygame.Surface(canva_size) # 3:2
        self.cva_rect = self.canva.get_rect()

        self.height_meter = 0

        self.normal_health = sprite_at("sprite/heart-ui.png", (0,0,32,48))
        self.regen_health = sprite_at("sprite/heart-ui.png", (32,0,32,48))

        self.normal_power = load_sheet("sprite/power-ui.png", (0,0,64,64), 2)
        self.extra_power = load_sheet("sprite/power-ui.png", (0,0,64,64), 1, start_at=2)

        self.update_surface(scale)

        self.offset = [0,0]
        self.scroll_pos = [0,0]
        self.dt = 1

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

        self.block_sprites = pygame.sprite.Group()
        self.plat_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.health_ui_sprites = pygame.sprite.Group()
        self.power_ui_sprites = pygame.sprite.Group()

    def update_surface(self, win_scale):
        self.screen = pygame.display.get_surface()
        self.scr_size = pygame.display.get_window_size()

        cva_w = (((self.scr_size[0] // 15) * 8) // 128) * 128
        cva_h = (cva_w // 4) * 5

        self.cva_rect = pygame.Rect((self.scr_size[0] - cva_w) // 2, (self.scr_size[1] - cva_h) // 2, cva_w, cva_h)
        self.cva_scale = (self.canva.get_width() / cva_w, self.canva.get_height() / cva_h)
        self.win_scale = win_scale
        
        sw, sh = self.win_scale

        self.font = pygame.font.SysFont(None, int(30*sh))

        self.height_rect = pygame.Rect(30*sw, 30*sh, 200*sw, 50*sh)

        self.health_rect = pygame.Rect(30*sw, self.height_rect.bottom + 12*sh, 32*sw, 48*sh)
        self.health_offset = (44*sw, 0*sh)

        self.power_rect = pygame.Rect(30*sw, self.scr_size[1] - 94*sh, 64*sw, 64*sh)
        self.power_offset = (0*sw, 76*sh)

    def init_level(self):
        self.running = True
        self.height_meter = 0
        self.score = {'height':0,
                      'enemy':{'ght':0,'imp':0},
                      'item':{'ts1':0,'th1':0},
                      'health':0
                     }

        self.player = Player((150,320))

        self.offset[0] = 0
        self.offset[1] = self.player.rect.centery - (self.canva.get_height()*3/5)
        self.scroll_pos[0] = 0
        self.scroll_pos[1] = self.player.rect.centery - (self.canva.get_height()*3/5)

        # Load level data
        self.level = list()
        level_data = gen_level('data/map.json')
        for layer in level_data:
            layer_data = list()
            for data in layer:
                if data[0] in ['n1b','n2b','n3b']:
                    layer_data.append(Platform((data[2],self.canva.get_height()-data[3]),self.plat_data.data[data[0]]))
                elif data[0] == 'ght':
                    layer_data.append(Ghost('ght',(data[2],self.canva.get_height()-data[3])))
                elif data[0] == 'imp':
                    layer_data.append(Imp('imp',(data[2],self.canva.get_height()-data[3])))
                elif data[0] == 'td1':
                    layer_data.append(ItemDash('td1',(data[2],self.canva.get_height()-data[3])))
                elif data[0] == 'th1':
                    layer_data.append(ItemHealth('th1',(data[2],self.canva.get_height()-data[3])))
                elif data[0] == 'ts1':
                    layer_data.append(ItemScore('ts1',(data[2],self.canva.get_height()-data[3])))
                elif data[0] == 'prt':
                    layer_data.append(Portal((data[2],self.canva.get_height()-data[3])))
            self.level.append(layer_data)

        # Create on screen level  
        self.plat_sprites.empty()
        self.enemy_sprites.empty()
        self.item_sprites.empty()
        self.next_plat = len(self.level) - 1
        for i in range(5):
            self.make_layer(self.level[self.next_plat])
            self.next_plat -= 1

        self.danger_zone = DangerZone((0,self.player.rect.bottom), (self.canva.get_width(), self.canva.get_height()//3))

        self.portal = None

        # init UI
        self.health_ui_sprites.empty()
        self.health_index = 0
        for i in range(self.player.health):
            rect = self.health_rect.copy()
            rect.x += self.health_offset[0] * i
            self.health_index += 1
            self.health_ui_sprites.add(HealthUI(self.health_index, rect, self.normal_health))

        self.power_ui_sprites.empty()
        self.power_index = 0
        for i in range(self.player.power_default):
            rect = self.power_rect.copy()
            rect.y -= self.power_offset[1] * i
            self.power_index += 1
            self.power_ui_sprites.add(PowerUI(1, self.power_index, rect, self.normal_power))
        
    
    def make_layer(self, layer):
        for data in layer:
            if isinstance(data, Platform):
                self.plat_sprites.add(data)
            elif isinstance(data, (Ghost,Imp)):
                self.enemy_sprites.add(data)
            elif isinstance(data, (ItemDash,ItemHealth,ItemScore)):
                self.item_sprites.add(data)
            elif isinstance(data, (Portal)):
                self.portal = data

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
        self.item_sprites.update(self.dt)
        self.player.update(self.dt)
        self.particles.update(self.dt)
        self.scroll(self.dt)

        # collide enemies
        for enemy in self.enemy_sprites.sprites():
            rm_enemy = False
            if enemy.hitbox.colliderect(self.player.rect):
                if self.player.dashing:
                    rm_enemy = True
                elif not self.player.immunity:
                    if self.player.vel.y > 0:
                        if self.player.rect.bottom <= enemy.rect.centery or self.player.vel.y > enemy.rect.height // 2:
                            rm_enemy = True
                    else:
                        self.player.damaged = True

            if rm_enemy:
                self.score['enemy'][enemy.name] += 1
                self.enemy_sprites.remove(enemy)

        # collide items
        for item in self.item_sprites.sprites():
            if item.hitbox.colliderect(self.player.rect):
                effect = item.amount
                if isinstance(item, (ItemDash)):
                    for i in range(effect):
                        if self.player.power_amount < self.player.power_max:
                            self.player.power_amount += 1
                        else:
                            break
                elif isinstance(item, (ItemHealth)):
                    if self.player.health + self.player.rg_health == self.player.max_health:
                        self.score['item'][item.name] += 1
                    else:
                        for i in range(effect):
                            if self.player.health + self.player.rg_health < self.player.max_health:
                                self.player.rg_health += 1
                            else:
                                break
                elif isinstance(item, (ItemScore)):
                    for i in range(effect):
                        self.score['item'][item.name] += 1

                self.item_sprites.remove(item)

        # update UI
        current_height = (self.canva.get_height() - self.player.rect.bottom) * 10 // 32
        if current_height > self.height_meter:
            self.height_meter = current_height

        self.height_text = self.font.render(f'Height : {self.height_meter}', True, (0,0,0))

        self.health_ui_sprites.update(self.player)
        self.power_ui_sprites.update(self.player)
        # Add regen health UI
        for i in range(self.health_index, self.player.health + self.player.rg_health):
            rect = self.health_rect.copy()
            rect.x += self.health_offset[0] * i
            self.health_index += 1
            self.health_ui_sprites.add(HealthUI(self.health_index, rect, self.regen_health))
        # Add extra power UI
        for i in range(self.power_index, self.player.power_amount):
            rect = self.power_rect.copy()
            rect.top -= self.power_offset[1] * i
            self.power_index += 1
            self.power_ui_sprites.add(PowerUI(2, self.power_index, rect, self.extra_power))
        # Remove health UI
        for health_ui in self.health_ui_sprites.sprites():
            if not health_ui.show:
                self.health_ui_sprites.remove(health_ui)
                self.health_index -= 1
        # Remove extra power UI
        for power_ui in self.power_ui_sprites.sprites():
            if power_ui.type == 2 and not power_ui.recharge:
                self.power_ui_sprites.remove(power_ui)
                self.power_index -= 1

        # for i in self.power_ui_sprites.sprites():
        #     print(i.pos, end=" ")
        # print(self.player.power_amount)
        # print(len(self.health_ui_sprites.sprites()), self.player.health, self.player.rg_health)
        # print(self.height_meter)

        # Level loading
        top_plat = 320
        # Remove off screen platforms
        for platform in self.plat_sprites.sprites():
            if self.player.rect.bottom - platform.rect.top < -96 and self.player.hit_ground: # 48 * 2
                self.plat_sprites.remove(platform)
            if platform.rect.bottom < top_plat:
                top_plat = platform.rect.bottom
        # Remove off screen enemies
        for enemy in self.enemy_sprites.sprites():
            if self.player.rect.bottom - enemy.rect.top < -96 and self.player.hit_ground: # 48 * 2
                self.enemy_sprites.remove(enemy)      
        # Make next layer
        if top_plat - self.player.rect.top > - 128: # 48 * 3 - 16
            self.make_layer(self.level[self.next_plat])
            if self.next_plat > 0:
                self.next_plat -= 1

        # Update danger zone
        if self.player.hit_ground:
            self.danger_zone.update_height(self.player.rect.midbottom)
        self.danger_zone.update(self.dt)

        if self.portal is not None:
            self.portal.update(self.dt)

        # print(len(self.enemy_sprites.sprites()), len(self.plat_sprites.sprites()), len(self.item_sprites.sprites()))
        print(self.score)

        if self.player.health == 0:
            self.running = False

    def draw(self):
        self.canva.fill((0,0,100))

        # for i in range(7):
        #     pygame.draw.rect(self.canva, (200,155,155),pygame.Rect(32*i,100,32,32+i*10))
        # for i in range(10):
        #     pygame.draw.rect(self.canva, (25*i,255,255//(i+1)),pygame.Rect(224,32*i,32,32))

        for platform in self.plat_sprites:
            self.canva.blit(platform.image, (platform.rect.x-self.offset[0], platform.rect.y-self.offset[1]))
        for enemy in self.enemy_sprites:
            self.canva.blit(enemy.image, (enemy.rect.x-self.offset[0], enemy.rect.y-self.offset[1]))
        for item in self.item_sprites:
            self.canva.blit(item.image, (item.rect.x-self.offset[0], item.rect.y-self.offset[1]))
        self.player.draw(self.canva, self.offset)
        self.particles.draw(self.canva)
        self.danger_zone.draw(self.canva, self.offset)
        if self.portal is not None:
            self.canva.blit(self.portal.image, (self.portal.rect.x-self.offset[0], self.portal.rect.y-self.offset[1]))

        self.screen.blit(pygame.transform.scale(self.canva, self.cva_rect.size), self.cva_rect.topleft)

        pygame.draw.rect(self.screen, (255,255,255),self.height_rect)
        self.screen.blit(self.height_text, self.height_text.get_rect(midleft=(self.height_rect.x+self.height_rect.width//10, self.height_rect.y+self.height_rect.height//2)))
        self.health_ui_sprites.draw(self.screen)
        self.power_ui_sprites.draw(self.screen)

    def scroll(self, dt):
        # Lock offset Y
        self.offset[1] += ((self.player.rect.centery - self.offset[1] - (self.canva.get_height()*3/5)) / 5) * dt 

        # if self.player.hit_ground:
        #     self.scroll_pos[1] = self.player.rect.centery
            
        # # Lock offset Y
        # if self.offset[1] != self.scroll_pos[1]:
        #     self.offset[1] += ((self.scroll_pos[1] - self.offset[1] - (self.canva.get_height()*3/5)) / 10) * dt
        # else:
        #     s
