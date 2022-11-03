import pygame, base64, json
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

        self.current_menu = [self.main_menu, self.game_loop, self.rank_menu, self.option_menu, self.score_menu]
        self.id = 0
        self.pause = False

        with open('data/rank.json', 'rb') as f:
            # load data str
            try:
                self.rank_data = json.load(f)
                # decode to base64 then decode to str
                self.rank_data = base64.b64decode(self.rank_data).decode('utf-8')
                # convert to dict
                self.rank_data = json.loads(self.rank_data)
            except json.decoder.JSONDecodeError:
                print(1)
                self.rank_data = dict()
            f.close()

        self.main_menu_button = pygame.sprite.Group()
        self.option_menu_button = pygame.sprite.Group()
        self.pause_menu_button = pygame.sprite.Group()
        self.back_button = None
        self.set_menu()

        self.game = Game((256,320), self.scale)
        self.new_game = True
        self.run = True

    def set_menu(self):
        sw, sh = self.scale
        self.fontL = pygame.font.SysFont(None, int(30*sh))
        self.fontM = pygame.font.SysFont(None, int(25*sh))

        self.back_button = Button(self.scr_size[0] - 80*sw, 30*sh, 50*sw, 50*sh, (200,155,155), self.fontL, '->')

        self.main_menu_button.empty()
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 370*sh, 200*sw, 50*sh, (40,50,150), self.fontL, 'Play'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 290*sh, 200*sw, 50*sh, (40,50,150), self.fontL, 'Ranking'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 210*sh, 200*sw, 50*sh, (40,50,150), self.fontL, 'Options'))
        self.main_menu_button.add(Button(80*sw, self.scr_size[1] - 130*sh, 200*sw, 50*sh, (40,50,150), self.fontL, 'Exit'))

        self.option_menu_button.empty()
        self.option_menu_button.add(Button(80*sw, 200*sh, 100*sw, 50*sh, (40,50,150), self.fontM, f'{self.scr_option[0][0]}x{self.scr_option[0][1]}'))
        self.option_menu_button.add(Button(80*sw, 280*sh, 100*sw, 50*sh, (40,50,150), self.fontM, f'{self.scr_option[1][0]}x{self.scr_option[1][1]}'))
        self.option_menu_button.add(Button(80*sw, 360*sh, 100*sw, 50*sh, (40,50,150), self.fontM, f'{self.scr_option[2][0]}x{self.scr_option[2][1]}'))
        self.option_menu_button.add(Button(80*sw, 440*sh, 100*sw, 50*sh, (40,50,150), self.fontM, f'{self.scr_option[3][0]}x{self.scr_option[3][1]}'))

        self.rank_board = pygame.Surface((760*sw,600*sh))
        self.rank_board.fill((200,155,155))

        self.pause_menu_button.empty()
        self.pause_menu_button.add(Button(self.scr_size[0]//2 - 75*sw, 200*sh, 150*sw, 50*sh, (40,50,150), self.fontL, 'Resume'))
        self.pause_menu_button.add(Button(self.scr_size[0]//2 - 75*sw, 280*sh, 150*sw, 50*sh, (40,50,150), self.fontL, 'Back to Title'))
        self.pause_menu_tint = pygame.Surface(self.scr_size, pygame.SRCALPHA)
        self.pause_menu_tint.fill((77, 77, 92))
        self.pause_menu_tint.set_alpha(120)

    def run_menu(self, event_list, dt):
        if self.id == 1 and self.new_game:
            self.game.init_level()
            self.score = dict()
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
        if not self.pause:
            self.back_button.update(event_list)

            if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked():
                self.pause = True
                self.game.reset_player_move()

            self.game.update(event_list, dt)

            if not self.game.running:
                self.calculate_score()
                self.id = 4
                self.new_game = True
            
        self.screen.fill((30,30,30))
        self.game.draw()

        if self.pause:
            self.pause_menu(event_list)
        else:
            self.back_button.draw(self.screen)

    def rank_menu(self, event_list, _):
        sw, sh = self.scale
        self.back_button.update(event_list)

        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked():
            self.id = 0
            
        self.screen.fill((200,220,255))
        self.back_button.draw(self.screen)
        self.screen.blit(self.rank_board, ((self.scr_size[0]-760*sw)/2,(self.scr_size[1]-600*sh)/2))

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
                self.set_menu()
                self.game.update_surface(self.scale)
  
        self.screen.fill((100,220,155))
        self.back_button.draw(self.screen)
        self.option_menu_button.draw(self.screen)

    def score_menu(self, event_list, _):
        self.back_button.update(event_list)

        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.back_button.get_clicked():
            self.id = 0

            anyms_c = 1
            for name in self.rank_data:
                if name.startswith('anonymous') and anyms_c < 5:
                    anyms_c += 1

            if self.rank_data[f'anonymous{anyms_c}'] < self.score['all']:
                self.rank_data[f'anonymous{anyms_c}'] = self.score['all']

            while len(self.rank_data) > 5:
                rm_name = min(self.rank_data, key=self.rank_data.get)
                print(rm_name)
                self.rank_data.pop(rm_name)

            with open('data/rank.json', 'w') as f:
                data = self.rank_data
                # convert to json dict then encode to byte
                data = json.dumps(data).encode('utf-8')
                # encode to base64 then decode to str
                data = base64.b64encode(data).decode('utf-8')
                # write to file
                json.dump(data, f)
                f.close()

            print(self.rank_data)

        self.screen.fill((100,220,155))
        self.back_button.draw(self.screen)

    def pause_menu(self, event_list):
        self.pause_menu_button.update(event_list)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.pause = False
        for i, button in enumerate(self.pause_menu_button.sprites()):
            if button.get_clicked():
                if i == 1:
                    self.game.quit_game()
                    self.calculate_score()
                    self.id = 4
                    self.new_game = True
                self.pause = False

        self.screen.blit(self.pause_menu_tint, (0,0))
        self.pause_menu_button.draw(self.screen)

    def calculate_score(self):
        score_data = self.game.score_data

        self.score['height'] = int(score_data['height'] * 0.7)
        self.score['enemy'] = dict()
        self.score['enemy']['ght'] = score_data['enemy']['ght'] * 100
        self.score['enemy']['imp'] = score_data['enemy']['imp'] * 300
        self.score['item'] = dict()
        self.score['item']['ts1'] = score_data['item']['ts1'] * 200
        self.score['item']['th1'] = score_data['item']['th1'] * 150

        self.score['health'] = 0
        if score_data['height'] >= 100:
            self.score['health'] = score_data['health'] * 100

        self.score['all'] = self.score['height']+self.score['enemy']['ght']+self.score['enemy']['imp']+\
                            self.score['item']['ts1']+self.score['item']['th1']+self.score['health']

        print(self.score)
