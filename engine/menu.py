import pygame
from engine.game import Game

class Menu():
    def __init__(self):    
        self.crnMenu = [self.main_menu, self.game_loop, self.option_menu]
        self.Id = 0

        self.scrOption = [(1200,960),(1080,840),(960,720),(840,600)]
        self.scrId = 2

        self.scrSize = self.scrOption[self.scrId]
        self.screen = pygame.display.set_mode(self.scrSize, 0, 32)

        self.game = Game()
        self.run = True

    def run_menu(self, dt):
        self.crnMenu[self.Id](dt)

    def main_menu(self, _):
        playB = pygame.Rect(50,50,200,50)
        optionB = pygame.Rect(50,150,100,50)
        exitB = pygame.Rect(50,250,70,50)

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if playB.collidepoint(mx, my):
                self.Id = 1
            elif optionB.collidepoint(mx, my):
                self.Id = 2
            elif exitB.collidepoint(mx, my):
                self.run = False
            
        self.screen.fill((200,220,255))
        pygame.draw.rect(self.screen, (200,155,155), playB)
        pygame.draw.rect(self.screen, (200,155,155), optionB)
        pygame.draw.rect(self.screen, (200,155,155), exitB)

    def game_loop(self, dt):
        backB = pygame.Rect(self.scrSize[0]-100,50,50,50)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Id = 0
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if backB.collidepoint(mx, my):
                self.Id = 0

        self.game.update(dt)
            
        self.screen.fill((30,30,30))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        self.game.draw()

    def option_menu(self, _):
        backB = pygame.Rect(self.scrSize[0]-100,50,50,50)
        resB = []
        for i in range(4):
            resB.append(pygame.Rect(50,(i*100)+50, 100,50))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Id = 0
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if backB.collidepoint(mx, my):
                self.Id = 0
            for i, button in enumerate(resB):
                if button.collidepoint(mx, my):
                    self.scrId = i
                    self.scrSize = self.scrOption[self.scrId]
                    self.screen = pygame.display.set_mode(self.scrSize, 0, 32)
                    self.game.update_canva()
  
        self.screen.fill((100,220,155))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        for button in resB:
            pygame.draw.rect(self.screen, (200,155,155), button)