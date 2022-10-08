import pygame, sys, random
from particle import SplashVFX

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('particle')
screen = pygame.display.set_mode((500, 500), 0, 32)

particleType = {'ptw': [1, (2,5), (180,360), 5, 0.1, (0   ,0.2), (255,255,255), False, False],
                'pte': [1, (3,7), (  0,360), 8, 0.1, (0.1 ,0.3), (255,155,155), False, True ],
                'ptr': [1, (4,6), (  0,360), 4, 0.1, (0   ,0  ), (155,255,155), (50,50,50), False],
                'ptt': [1, (2,3), (260,280), 6, 0.1, (0   ,0  ), (155,155,255), (20,20,20), False],
                'pty': [1, (1,2), (200,340), 5, 0.05,(-1 ,-0.1), (200,100,100), (60,30,10), True]}

particles = []
typed = [key for key in particleType]
index = 0
particleTime = 1

while True:
    screen.fill((0,0,0))

    for i, particle in reversed(list(enumerate(particles))):
            particle.update(1)
            particle.draw(screen)
            if not particle.alive:
                particles.pop(i)

    mx, my = pygame.mouse.get_pos()

    ptc = particleType[typed[index]]
    for i in range(particleTime):
        particles.append(SplashVFX(ptc[0],[mx, my],random.randint(ptc[1][0],ptc[1][1]),random.randint(ptc[2][0],ptc[2][1]),ptc[3],ptc[4],ptc[5],ptc[6],ptc[7],ptc[8]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_e:
                index += 1
            if event.key == pygame.K_q:
                index -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            lmb = pygame.mouse.get_pressed()[0]
            mmb = pygame.mouse.get_pressed()[1]
            rmb = pygame.mouse.get_pressed()[2]
            if lmb:
                particleTime += 1
            if rmb:
                particleTime -= 1
            if mmb:
                for i in range(20):
                    particles.append(SplashVFX(ptc[0],[mx,my],random.randint(ptc[1][0],ptc[1][1]),random.randint(ptc[2][0],ptc[2][1]),ptc[3],ptc[4],ptc[5],ptc[6],ptc[7],ptc[8]))

    index = 0 if index > len(typed)-1 else len(typed)-1 if index < 0 else index

    pygame.display.flip()
    clock.tick(60)