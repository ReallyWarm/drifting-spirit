import pygame
from engine.game import Game

class Menu():
    def __init__(self):    
        self.crnMenu = [self.main_menu, self.game_loop, self.rank_menu, self.option_menu]
        self.Id = 0

        self.scrOption = [(1200,960),(1080,840),(960,720), (840,600)]
        self.scrId = 2

        self.scrSize = self.scrOption[self.scrId]
        self.screen = pygame.display.set_mode(self.scrSize, 0, 32)

        self.game = Game()
        self.mouseDown = False
        self.run = True

    def run_menu(self, dt):
        self.crnMenu[self.Id](dt)

    def get_mouse_down(self, index): 
        if pygame.mouse.get_pressed()[index]:
            if not self.mouseDown:
                self.mouseDown = True
                return True
            else:
                return False
        self.mouseDown = False
        return False

    def main_menu(self, _):
        playB = pygame.Rect(80,self.scrSize[1]-370,200,45)
        rankB = pygame.Rect(80,self.scrSize[1]-290,150,45)
        optionB = pygame.Rect(80,self.scrSize[1]-210,100,45)
        exitB = pygame.Rect(80,self.scrSize[1]-130,70,45)

        mx, my = pygame.mouse.get_pos()
        if self.get_mouse_down(0):
            if playB.collidepoint(mx, my):
                self.Id = 1
            elif rankB.collidepoint(mx, my):
                self.Id = 2
            elif optionB.collidepoint(mx, my):
                self.Id = 3
            elif exitB.collidepoint(mx, my):
                self.run = False
            
        self.screen.fill((200,220,255))
        pygame.draw.rect(self.screen, (200,155,155), playB)
        pygame.draw.rect(self.screen, (200,155,155), rankB)
        pygame.draw.rect(self.screen, (200,155,155), optionB)
        pygame.draw.rect(self.screen, (200,155,155), exitB)

    def game_loop(self, dt):
        backB = pygame.Rect(self.scrSize[0]-80,30,50,50)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Id = 0
        mx, my = pygame.mouse.get_pos()
        if self.get_mouse_down(0):
            if backB.collidepoint(mx, my):
                self.Id = 0

        self.game.update(dt)
            
        self.screen.fill((30,30,30))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        self.game.draw()

    def rank_menu(self, _):
        backB = pygame.Rect(self.scrSize[0]-80,30,50,50)
        boardB = pygame.Rect((self.scrSize[0]-640)/2,(self.scrSize[1]-510)/2,640,510)

        mx, my = pygame.mouse.get_pos()
        if self.get_mouse_down(0):
            if backB.collidepoint(mx, my):
                self.Id = 0
            
        self.screen.fill((200,220,255))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        pygame.draw.rect(self.screen, (200,155,155), boardB)

    def option_menu(self, _):
        backB = pygame.Rect(self.scrSize[0]-80,30,50,50)
        resB = []
        for i in range(4):
            resB.append(pygame.Rect(80,(i*80)+150, 100,50))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Id = 0
        mx, my = pygame.mouse.get_pos()
        if self.get_mouse_down(0):
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