import sys
from math import sin
from random import uniform, random
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPS_CLOCK = pygame.time.Clock()


class Snow:
    """snow flake object"""

    def __init__(self):
        self.pos_x = uniform(0, 600)
        self.pos_y = -10
        self.drift = random()
        self.speed = uniform(0, 5) + 1
        self.width = uniform(0, 3) + 2
        self.height = self.width
        self.theta = uniform(0, 100)
        self.radius = uniform(0, 10) + 3

    def draw(self):
        x_offset = sin(self.theta) * self.radius
        rect = Rect(self.pos_x + x_offset, self.pos_y, self.width, self.height)
        color = int(self.width / 5 * 225)
        pygame.draw.ellipse(SURFACE, (color, color, color), rect)

    def move(self):
        self.pos_y += self.speed
        if self.pos_y > 600:
            self.pos_y = -5
        self.pos_x += self.drift
        if self.pos_x > 600:
            self.pos_x = 0
        self.theta += 0.1


def main():
    counter = 0
    snows = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter += 1
        if counter % 10 == 0 and len(snows) < 100:
            snows.append(Snow())
        for snow in snows:
            snow.move()

        SURFACE.fill((0, 0, 0))
        for snow in snows:
            snow.draw()

        pygame.display.update()
        FPS_CLOCK.tick(15)


if __name__ == '__main__':
    main()
