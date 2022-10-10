import pygame
from engine.graphic.particlelist import ParticleList

class Game():
    def __init__(self):
        self.canva = pygame.Surface((576,720))
        self.cvaRect = self.canva.get_rect()
        self.sclCanva = (0,0)
        self.update_canva()

        self.particles = ParticleList()
        self.particles.new_type('flame0',1,[1,(1,2),(250,290), 5, 0.05,(-1,-0.1),(255,120, 60), (55,25,15), True])
        self.particles.new_type('spark0',1,[2,(3,4),(  0,360), 3, 0.05,     None,(200,200,100), False, False])
        self.particles.new_type('dusts0',1,[1,(2,5),(180,360), 5, 0.1 ,(0  ,0.2),(255,255,255), False, False])
        self.ptcId = 'flame0'

    def update_canva(self):
        self.screen = pygame.display.get_surface()
        self.scrSize = pygame.display.get_window_size()
        self.cvaRect.size = ((self.scrSize[0] // 5) * 3, self.scrSize[1])
        self.cvaRect.topleft = ((self.scrSize[0] - self.cvaRect.width) // 2, 0)
        self.sclCanva = (self.canva.get_width() / self.cvaRect.width, self.canva.get_height() / self.cvaRect.height)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.ptcId = 'flame0'
        if keys[pygame.K_w]:
            self.ptcId = 'spark0'
        if keys[pygame.K_e]:
            self.ptcId = 'dusts0'

        mx, my = pygame.mouse.get_pos()
        if self.cvaRect.collidepoint(mx, my):
            if pygame.mouse.get_pressed()[0]:
                for i in range(5):
                    self.particles.add(self.ptcId, [(mx-self.cvaRect.x)*self.sclCanva[0], (my-self.cvaRect.y)*self.sclCanva[1]])

    def update(self, dt):
        self.input()
        self.particles.update(dt)

    def draw(self):
        rect1 = pygame.Rect(self.canva.get_width()-50,50,50,50)

        self.canva.fill((0,0,100))
        pygame.draw.rect(self.canva, (100,0,0), rect1)
        self.particles.draw(self.canva)
        self.screen.blit(pygame.transform.scale(self.canva, self.cvaRect.size), self.cvaRect.topleft)