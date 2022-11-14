import pygame, sys, os, random
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(MAIN_DIR))
from engine.bullet import BulletList

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('bullet')
screen = pygame.display.set_mode((500, 500), 0, 32)

box = pygame.Rect(200,200,50,50)
bullets = BulletList(image=pygame.image.load("sprite/bullet.png").convert_alpha())
draw = False

while True:
    screen.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_e:
                pass
            if event.key == pygame.K_q:
                pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            lmb = pygame.mouse.get_pressed()[0]
            mmb = pygame.mouse.get_pressed()[1]
            rmb = pygame.mouse.get_pressed()[2]
            if lmb:
                bullets.add([mx,my], 32, 5, 180,time=200,color=(255,255,255),particle=False)
            if rmb:
                pass
            if mmb:
                pass

    # for b in bullets.bullets:
    #     if b.rect.collidepoint(mx,my):
    #         print(1)
    #     print(0)
    
    pygame.draw.rect(screen, (100,255,100), box)
    bullets.update(1, [box])
    # a = bullets.get_collide()
    # print(a)
    # print(bullets.bullets)
    bullets.draw(screen)

    pygame.display.flip()
    clock.tick(60)