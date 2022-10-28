import pygame
from engine.game import Game
from engine.graphic.gameui import Button

class Menu():
    def __init__(self, scr_id=1):
        self.scr_option = [(1440,960),(1200,800),(960,640),(720,480)] # 3:2
        self.scr_id = scr_id

        self.scr_size = self.scr_option[self.scr_id]
        self.scr_default = self.scr_size
        self.screen = pygame.display.set_mode(self.scr_size, 0, 32)
        self.scale = (1,1)

        self.current_menu = [self.main_menu, self.game_loop, self.rank_menu, self.option_menu]
        self.id = 0

        self.main_menu_button = pygame.sprite.Group()
        self.option_menu_button = pygame.sprite.Group()
        self.back_button = None
        self.set_button()

        self.game = Game((256,320), self.scale)
        self.new_game = True
        self.run = True

    def set_button(self):
        sw, sh = self.scale
        self.fontM = pygame.font.SysFont(None, int(30*sh))
        self.fontOp = pygame.font.SysFont(None, int(25*sh))

        self.back_button = Button(self.scr_size[0] - 80*sw, 30*sh, 50*sw, 50*sh, (200,155,155), self.fontM, '->')

        self.main_menu_button.empty()
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 370*sh, 200*sw, 50*sh, (40,50,150), self.fontM, 'Play'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 290*sh, 200*sw, 50*sh, (40,50,150), self.fontM, 'Ranking'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 210*sh, 200*sw, 50*sh, (40,50,150), self.fontM, 'Options'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 130*sh, 200*sw, 50*sh, (40,50,150), self.fontM, 'Exit'))

        self.option_menu_button.empty()
        self.option_menu_button.add(Button(80*sw, 150*sh, 100*sw, 50*sh, (40,50,150), self.fontOp, f'{self.scr_option[0][0]}x{self.scr_option[0][1]}'))
        self.option_menu_button.add(Button(80*sw, 230*sh, 100*sw, 50*sh, (40,50,150), self.fontOp, f'{self.scr_option[1][0]}x{self.scr_option[1][1]}'))
        self.option_menu_button.add(Button(80*sw, 310*sh, 100*sw, 50*sh, (40,50,150), self.fontOp, f'{self.scr_option[2][0]}x{self.scr_option[2][1]}'))
        self.option_menu_button.add(Button(80*sw, 390*sh, 100*sw, 50*sh, (40,50,150), self.fontOp, f'{self.scr_option[3][0]}x{self.scr_option[3][1]}'))

    def run_menu(self, event_list, dt):
        if self.id == 1 and self.new_game:
            self.game.init_level()
            self.new_game = False

        self.current_menu[self.id](event_list, dt)

    def main_menu(self, event_list, _):
        self.main_menu_button.update(event_list)

        for i, button in enumerate(self.main_menu_button.sprites()):
            if button.get_clicked():
                if i == 3:
                    self.run = False
                elif i == 0:
                    self.id = 1
                elif i == 1:
                    self.id = 2
                elif i == 2:
                    self.id = 3
            
        self.screen.fill((200,220,255))
        self.main_menu_button.draw(self.screen)

    def game_loop(self, event_list, dt):
        self.back_button.update(event_list)

        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked() or not self.game.running:
            self.id = 0
            self.new_game = True

        self.game.update(event_list, dt)
            
        self.screen.fill((30,30,30))
        self.game.draw()
        self.back_button.draw(self.screen)

    def rank_menu(self, event_list, _):
        sw, sh = self.scale
        self.back_button.update(event_list)
        boardB = pygame.Rect((self.scr_size[0]-760*sw)/2,(self.scr_size[1]-600*sh)/2,760*sw,600*sh)

        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked():
            self.id = 0
            
        self.screen.fill((200,220,255))
        self.back_button.draw(self.screen)
        pygame.draw.rect(self.screen, (200,155,155), boardB)

    def option_menu(self, event_list, _):
        self.back_button.update(event_list)
        self.option_menu_button.update(event_list)

        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked():
            self.id = 0

        for i, button in enumerate(self.option_menu_button.sprites()):
            if button.get_clicked():
                self.scr_id = i
                self.scr_size = self.scr_option[self.scr_id]
                self.scale = (self.scr_size[0] / self.scr_default[0], self.scr_size[1] / self.scr_default[1])
                self.screen = pygame.display.set_mode(self.scr_size, 0, 32)
                self.set_button()
                self.game.update_surface(self.scale)
  
        self.screen.fill((100,220,155))
        self.back_button.draw(self.screen)
        self.option_menu_button.draw(self.screen)