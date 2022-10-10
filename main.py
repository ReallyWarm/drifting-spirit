import pygame, sys
from engine.menu import Menu

FPS = 60

class GameWindow():
    def __init__(self):
        pygame.init()

        self.gameMenu = Menu()
        pygame.display.set_caption('Drifting Spirit')

        self.clock = pygame.time.Clock()

    def run(self):
        delta = 1000//FPS
        while self.gameMenu.run:
            pygame.display.set_caption(f'Drifting Spirit [{round(self.clock.get_fps())}]')
            dt = 60/1000 * delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameMenu.run = False

            self.gameMenu.run_menu(dt)

            pygame.display.flip()
            delta = self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = GameWindow()
    game.run()
