import pygame, sys
from engine.menu import Menu

class GameWindow():
    def __init__(self):
        pygame.init()

        self.fps = 60
        self.delta = 1000//self.fps
        self.gameMenu = Menu()
        pygame.display.set_caption('Drifting Spirit')

        self.clock = pygame.time.Clock()

    def update_fps(self):
        fps = self.gameMenu.get_fps()
        if self.fps != fps:
            self.fps = fps
            self.delta = 1000//self.fps

    def run(self):
        while self.gameMenu.run:
            pygame.display.set_caption(f'Drifting Spirit [{round(self.clock.get_fps())}]')
            self.update_fps()
            dt = 60/1000 * self.delta

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.gameMenu.run = False

            self.gameMenu.run_menu(event_list, dt)

            pygame.display.update()
            self.delta = self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = GameWindow()
    game.run()
