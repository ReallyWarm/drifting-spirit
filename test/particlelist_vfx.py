import pygame, sys, os
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(MAIN_DIR))
from engine.graphic.particlelist import ParticleList

FPS = 60

pygame.init()
pygame.display.set_caption('particlelist')
screen = pygame.display.set_mode((500, 500), 0, 32)
font = pygame.font.SysFont('Calibri',20)

particles = ParticleList()
particles.new_type('ptw',1,[1,(2,5),(180,360), 5, 0.1 ,(0  ,0.2),(255,255,255), False, False])
particles.new_type('pte',1,[1,(3,7),(  0,360), 8, 0.1 ,(0.1,0.3),(255,155,155), False, True])
particles.new_type('ptr',1,[1,(4,6),(  0,360), 4, 0.1 ,     None,(155,255,155), (50,50,50), False])
particles.new_type('ptt',1,[1,(2,3),(260,280), 6, 0.1 ,     None,(155,155,255), (20,20,20), False], 4)
particles.new_type('pty',1,[1,(1,2),(240,300), 5, 0.05,(-1,-0.1),(200,100,100), (60,30,10), True])
particles.new_type('ptu',1,[2,(3,4),(  0,360), 3, 0.05,     None,(200,200,100), False, False])
particles.new_type('pti',1,[2,(4,8),(135,405), 2, 0.1 ,(-0.2,-0.4),(60,90, 90), False, True])
particles.new_type('pto',1,[3,(3,4),(  0,360), 3, 0.05,     None,(200,100,200), False, False])
particles.new_type('ptp',1,[3,(2,6),(  0,360), 5, 0.1 ,(0.3,0.1),( 55,255,255), False, False])
particles.new_type('t1',1,[1,(1,2),(200,340),3,0.05,(0,0.2),(255,255,255),None,False],0)
particles.add_border((100, 400), (100, 400))

typed = particles.get_name()
index = 0
particleTime = 1

delta = 1000//FPS
clock = pygame.time.Clock()

while True:
    # delta time at 60 fps
    dt = 60/1000 * delta

    screen.fill((0,0,0))

    particles.update(dt)
    particles.draw(screen, [0,0])
    print(particles.particles)

    mx, my = pygame.mouse.get_pos()

    ptc = typed[index]
    for i in range(particleTime):
        particles.add(ptc, [mx, my], dt)

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
                ptc = typed[index]
                for i in range(20):
                    particles.add(ptc, [mx, my])

    index = 0 if index > len(typed)-1 else len(typed)-1 if index < 0 else index

    ptcName = font.render("Name: " + str(ptc), False, (255,255,255))
    screen.blit(ptcName, (5,5))
    pygame.display.set_caption(f'particlelist [{int(clock.get_fps())}]')
    pygame.display.flip()
    delta = clock.tick(FPS)
