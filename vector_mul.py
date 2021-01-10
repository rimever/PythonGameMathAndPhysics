import sys
from math import floor
import pygame
from pygame.locals import Rect, QUIT, MOUSEBUTTONDOWN

pygame.init()
SURFACE = pygame.display.set_mode((500, 550))
FPS_CLOCK = pygame.time.Clock()


class Slider:
    def __init__(self, rect, min_value, max_value, value):
        self.rect = rect
        self.slider_rect = rect.copy()
        self.slider_rect.inflate_ip(-20, -20)
        self.knob_rect = rect.copy()
        self.knob_rect.move_ip(10, 0)
        self.knob_rect.width = 4
        self.min_value = min_value
        self.max_value = max_value
        self.value = value

    def draw(self):
        pygame.draw.rect(SURFACE, (225, 225, 225), self.rect)
        pygame.draw.rect(SURFACE, (64, 64, 128), self.slider_rect)
        pygame.draw.rect(SURFACE, (0, 0, 255), self.knob_rect)

    def set_pos(self, pos_x):
        pos_x = max(self.slider_rect.left,
                    min(self.slider_rect.right, pos_x))
        pos_y = self.knob_rect.center[1]
        self.knob_rect.center = (pos_x, pos_y)

    def get_value(self):
        ratio = (self.knob_rect.center[0] - self.slider_rect.left) / self.slider_rect.width
        return (self.max_value - self.min_value) * ratio + self.min_value


def main():
    pos0 = (0, 0)
    pos1 = [0, 0]
    slider = Slider(Rect(20, 510, 460, 35), -3, 3, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if slider.rect.collidepoint(event.pos):
                    slider.set_pos(event.pos[0])
                else:
                    pos_x = floor((event.pos[0] - 240) / 25)
                    pos_y = floor((event.pos[1] - 240) / 25)
                    pos0 = (pos_x, pos_y)

        SURFACE.fill((0, 0, 0))
        slider.draw()
        for pos_y in range(0, 500, 25):
            for pos_x in range(0, 500, 25):
                pygame.draw.ellipse(SURFACE, (64, 64, 64), (pos_x, pos_y, 2, 2))

        pygame.draw.line(SURFACE, (255, 0, 0), (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (255, 0, 0), (0, 250), (500, 250), 3)

        coord0 = pos0[0] * 25 + 250, pos0[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 255, 0), (250, 250), coord0, 8)

        pos1[0] = pos0[0] * slider.get_value()
        pos1[1] = pos0[1] * slider.get_value()

        coord1 = pos1[0] * 25 + 250, pos1[1] * 25 + 250
        pygame.draw.line(SURFACE, (0, 0, 255), (250, 250), coord1, 2)

        pygame.display.update()
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
