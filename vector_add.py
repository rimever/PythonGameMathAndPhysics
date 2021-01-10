import sys
from math import floor
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()
SURFACE = pygame.display.set_mode((500, 500))
FPS_CLOCK = pygame.time.Clock()


def main():
    count = 0
    pos0 = (0, 0)
    pos1 = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos_x = floor((event.pos[0] - 240) / 25)
                pos_y = floor((event.pos[1] - 240) / 25)
                if count % 2 == 0:
                    pos0 = (pos_x, pos_y)
                    pos1 = (0, 0)
                else:
                    pos1 = (pos_x, pos_y)
                count += 1

        SURFACE.fill((0, 0, 0))
        for pos_x in range(0, 500, 25):
            for pos_y in range(0, 500, 25):
                pygame.draw.ellipse(SURFACE, (64, 64, 64), (pos_x, pos_y, 2, 2))

        pygame.draw.line(SURFACE, (255, 0, 0), (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (255, 0, 0), (0, 250), (500, 250), 3)

        coord0 = pos0[0] * 25 + 250, pos0[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 255, 0), (250, 250), coord0, 2)
        coord1 = pos1[0] * 25 + 250, pos1[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 255, 255), (250, 250), coord1, 2)
        coord2 = ((pos0[0] + pos1[0]) * 25 + 250, (pos0[1] + pos1[1]) * 25 + 250)
        pygame.draw.line(SURFACE, (255, 0, 255), (250, 250), coord2, 3)
        pygame.display.update()
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
