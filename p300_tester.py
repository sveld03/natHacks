import pygame, random, time
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

init_time = time.time()

pygame.init()
screen = pygame.display.set_mode((500, 500))
screen.fill(BLACK)

count = 0

color_choices = np.repeat(['RED', 'YELLOW', 'BLUE'], 7)
np.random.shuffle(color_choices)
np.random.shuffle(color_choices)

while count < 21:
    if (time.time() - init_time) >= 3:

        random_color = color_choices[count]

        if random_color == 'RED':
            pygame.draw.polygon(screen, RED, ((50,450),(250, 50),(450,450)))
        if random_color == 'YELLOW':
            pygame.draw.circle(screen, YELLOW, (250,250), 200)
        if random_color == 'BLUE':
            pygame.draw.rect(screen, BLUE, (50,50, 400, 400))

        pygame.display.update()
        time.sleep(0.5)
        screen.fill(BLACK)
        pygame.display.update()
        init_time = time.time()
        count += 1