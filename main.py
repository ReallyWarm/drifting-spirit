import pygame, sys
from random import randint

FPS = 60

screen_size = [960,720]
canva_size = [(screen_size[0]//5)*3,screen_size[1]]
canva_pos = [(screen_size[0]-canva_size[0])//2,0]

pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
canva = pygame.Surface((canva_size[0], canva_size[1]))
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    screen.fill('#71ddee')
    canva.fill('#ffffff')
    screen.blit(canva, (canva_pos[0], canva_pos[1]))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()