import pygame
import random

pygame.init()

screen_info = pygame.display.Info()
wi = screen_info.current_w
he = screen_info.current_h

WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
SIZE = [wi, he]
BLACK = [0, 0, 0]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snowfall")

snowFall = []
for i in range(2000):
    x = random.randrange(0, wi)
    y = random.randrange(0, he)
    speed = random.uniform(1, 1.5)
    color = [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)]
    baseSize = random.uniform(1, 2.1)
    snowFall.append([x, y, speed, color, baseSize])

clock = pygame.time.Clock()
done = False
mode = 0
size = 2
speedMult = 1
counter = 2000

def display_box(screen, message):
    font = pygame.font.Font(None, 25)
    text = font.render(message, True, GREEN)
    rect = pygame.Rect(0, 0, 200, 300)
    rect2 = pygame.Rect(0, 0, 203, 303)
    pygame.draw.rect(screen, WHITE, rect2)
    pygame.draw.rect(screen, BLACK, rect)
    modeText = ""
    if mode == 0:
        modeText = "Normal mode"
    elif mode == 1:
        modeText = "Colorful mode"
    elif mode == 2:
        modeText = "Flashing mode"
    if speedMult < 0:
        modeText += ", inverted"
    screen.blit(font.render(modeText, True, GREEN), (5, 5))
    screen.blit(text, (5, 30))
    screen.blit(font.render("Current size: " + str(size), True, GREEN), (5, 55))
    screen.blit(font.render("Snowflakes: " + str(counter), True, GREEN), (5, 80))
    screen.blit(font.render(str(round(clock.get_fps(), 0)) + " FPS", True, GREEN), (5, 105))
    screen.blit(font.render(str(round(1 / clock.get_fps() * 1000, 0)) + "ms latency", True, GREEN), (5, 130))
    if paused:
        screen.blit(font.render("Paused", True, GREEN), (5, 250))
        screen.blit(font.render("Press P to unpause", True, GREEN), (5, 275))
    elif energySaving:
        screen.blit(font.render("FPS limiter enabled", True, GREEN), (5, 250))
        screen.blit(font.render("Press END to disable", True, GREEN), (5, 275))

box_displayed = False
energySaving = False
paused = False
statbox = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_0:
                mode = 0
            if event.key == pygame.K_1:
                mode = 1
            if event.key == pygame.K_2:
                mode = 2
            if event.key == pygame.K_UP:
                size += 1
            if event.key == pygame.K_DOWN:
                size -= 1
            if event.key == pygame.K_LEFT and not paused:
                speedMult -= 0.25
            if event.key == pygame.K_RIGHT and not paused:
                speedMult += 0.25
            if event.key == pygame.K_INSERT and not paused:
                speedMult *= -1
            if event.key == pygame.K_PAGEUP:
                for i in range(100):
                    counter += 1
                    x = random.randrange(0, wi)
                    y = random.randrange(0, he)
                    speed = random.uniform(1, 1.5)
                    color = [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)]
                    snowFall.append([x, y, speed, color])
            if event.key == pygame.K_PAGEDOWN:
                if len(snowFall) >= 100:
                    for i in range(100):
                        counter -= 1
                        snowFall.pop()
            if event.key == pygame.K_HOME:
                if box_displayed:
                    box_displayed = False
                else:
                    box_displayed = True
            if event.key == pygame.K_END:
                if energySaving:
                    energySaving = False
                else:
                    energySaving = True
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                    speedMult = speedSaver
                else:
                    speedSaver = speedMult
                    speedMult = 0
                    paused = True
            if event.key == pygame.K_DELETE:
                mode = 0
                size = 2
                speedMult = 1
                counter = 2000

    screen.fill(BLACK)
    for i in range(len(snowFall)):
        if mode == 0:
            pygame.draw.circle(screen, [255, 255, 255], (snowFall[i][0], snowFall[i][1]), size * baseSize)
        elif mode == 1:
            pygame.draw.circle(screen, snowFall[i][3], (snowFall[i][0], snowFall[i][1]), size * baseSize)
        elif mode == 2 and not paused:
            pygame.draw.circle(screen, [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)], (snowFall[i][0], snowFall[i][1]), size * baseSize)
        elif mode == 2:
            pygame.draw.circle(screen, snowFall[i][3], (snowFall[i][0], snowFall[i][1]), size)
        if speedMult is not 0:
            snowFall[i][1] += random.uniform(snowFall[i][2] * 9 / 10, snowFall[i][2] * 11 / 10) * speedMult
        if speedMult > 0:
            if snowFall[i][1] > he:
                y = random.randrange(-50, -10)
                snowFall[i][1] = y

                x = random.randrange(0, wi)
                snowFall[i][0] = x
        else:
            if snowFall[i][1] < 0:
                y = random.randrange(he-50, he-10)
                snowFall[i][1] = y

                x = random.randrange(0, wi)
                snowFall[i][0] = x
    if box_displayed:
        display_box(screen, "Speed multiplier: " + str(round(speedMult, 2)) + "x")
    pygame.display.flip()
    if energySaving:
        clock.tick(30)
    else:
        clock.tick()
pygame.quit()
