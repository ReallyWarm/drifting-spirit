import pygame, sys, math

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('drawtest')
screen = pygame.display.set_mode((500, 500), 0, 32)

loc = [250, 250]
agv = 290
spd = 10
mxs = 10
scl = 20

while True:
    ang = math.radians(agv)
    screen.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()
    loc = [mx, my]

    points = [
    [loc[0] , loc[1]],
    [loc[0] - spd * scl * math.cos(ang + math.pi/6) *0.6, loc[1] - spd * scl * math.sin(ang + math.pi/6) *0.6],
    [loc[0] - spd * scl * math.cos(ang) * 3, loc[1] - spd * scl * math.sin(ang) * 3],
    [loc[0] - spd * scl * math.cos(ang - math.pi/6) *0.6, loc[1] - spd * scl * math.sin(ang - math.pi/6) *0.6],
    ]
    pygame.draw.polygon(screen, (255,255,255), points)
    pygame.draw.circle(screen, (255,0,0), points[0],2)
    pygame.draw.circle(screen, (0,255,0), points[1],2)
    pygame.draw.circle(screen, (0,0,255), points[2],2)
    pygame.draw.circle(screen, (155,155,155), points[3],2)

    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        agv += 1
    if keys[pygame.K_q]:
        agv -= 1
    if keys[pygame.K_z]:
        loc[0] -= 1
    if keys[pygame.K_x]:
        loc[0] += 1

    mb = pygame.mouse.get_pressed()
    if mb[0]:
        spd -= 0.1
    if mb[2]:
        spd += 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.key:
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
                pass
            if rmb:
                pass
            if mmb:
                pass

    pygame.display.flip()
    clock.tick(60)