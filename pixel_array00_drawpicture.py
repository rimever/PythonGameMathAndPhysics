import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((250, 250))
FPS_CLOCK = pygame.time.Clock()


def main():
    src = pygame.image.load("picture0.jpg").convert()
    while True:
        for _ in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
        SURFACE.blit(src, (0, 0))
        pygame.display.update()
        FPS_CLOCK.tick(5)


if __name__ == '__main__':
    main()
