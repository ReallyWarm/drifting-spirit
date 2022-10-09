import pygame, sys

FPS = 60

class Game():
    def __init__(self):
        pygame.init()
        
        self.scrOption = [(1200,960),(1080,840),(960,720),(840,600)]
        self.scrSize = (960,720)
        self.screen = pygame.display.set_mode(self.scrSize, 0, 32)

        self.cvaSize = ((self.scrSize[0] // 5) * 3, self.scrSize[1])
        self.cvaPos = ((self.scrSize[0] - self.cvaSize[0]) // 2, 0)
        self.canva = pygame.Surface((self.cvaSize[0], self.cvaSize[1]))

        self.crnMenu = [self.main_menu, self.game_loop, self.option_menu]
        self.menuId = 0

        self.clock = pygame.time.Clock()

    def run(self):
        run = True
        delta = 1000//FPS
        while run:
            dt = 60/1000 * delta

            exiting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exiting = True

            if exiting == True:
                if self.menuId == 0:
                    run = False 
                else:
                    self.menuId = 0

            self.crnMenu[self.menuId](dt)

            pygame.display.flip()
            delta = self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def game_loop(self, dt):
        backB = pygame.Rect(self.scrSize[0]-100,50,50,50)

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if backB.collidepoint(mx, my):
                self.menuId = 0
            
        self.screen.fill((30,30,30))
        self.canva.fill((255,255,255))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        self.screen.blit(self.canva, self.cvaPos)

    def main_menu(self, _):
        playB = pygame.Rect(50,50,200,50)
        optionB = pygame.Rect(50,150,100,50)

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if playB.collidepoint(mx, my):
                self.menuId = 1
            elif optionB.collidepoint(mx, my):
                self.menuId = 2
            
        self.screen.fill((200,220,255))
        pygame.draw.rect(self.screen, (200,155,155), playB)
        pygame.draw.rect(self.screen, (200,155,155), optionB)

    def option_menu(self, _):
        backB = pygame.Rect(self.scrSize[0]-100,50,50,50)
        resB = []
        for i in range(4):
            resB.append(pygame.Rect(50,(i*100)+50, 100,50))

        res_change = -1
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if backB.collidepoint(mx, my):
                self.menuId = 0
            for i, button in enumerate(resB):
                if button.collidepoint(mx, my):
                    res_change = i

        if res_change != -1:
            self.scrSize = self.scrOption[res_change]
            self.screen = pygame.display.set_mode(self.scrSize, 0, 32)
            self.cvaSize = ((self.scrSize[0] // 5) * 3, self.scrSize[1])
            self.cvaPos = ((self.scrSize[0] - self.cvaSize[0]) // 2, 0)
            self.canva = pygame.Surface((self.cvaSize[0], self.cvaSize[1]))
  
        self.screen.fill((100,220,155))
        pygame.draw.rect(self.screen, (200,155,155), backB)
        for button in resB:
            pygame.draw.rect(self.screen, (200,155,155), button)

if __name__ == '__main__':
    game = Game()
    game.run()