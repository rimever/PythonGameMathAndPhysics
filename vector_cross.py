import sys
from math import floor, hypot, asin, degrees
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()
SURFACE = pygame.display.set_mode((500, 700))
FPS_CLOCK = pygame.time.Clock()


def cross(vec1, vec2):
    """ベクトルの外積を返す"""
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]


def main():
    count = 0
    pos0 = (0, 0)
    pos1 = (0, 0)
    sys_font = pygame.font.SysFont(None, 24)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos_x = floor((event.pos[0] - 240) / 25)
                pos_y = -floor((event.pos[1] - 240) / 25)
                if count % 2 == 0:
                    pos0 = (pos_x, pos_y)
                    pos1 = (0, 0)
                else:
                    pos1 = (pos_x, pos_y)
                count += 1

        SURFACE.fill((0, 0, 0))
        for pos_y in range(0, 500, 25):
            for pos_x in range(0, 500, 25):
                pygame.draw.ellipse(SURFACE, (64, 64, 64), (pos_x, pos_y, 2, 2))
        pygame.draw.line(SURFACE, (255, 0, 0), (250, 0), (250, 500), 3)
        pygame.draw.line(SURFACE, (255, 0, 0), (0, 250), (500, 250), 3)
        coord0 = pos0[0] * 25 + 250, pos0[1] * -25 + 250
        pygame.draw.line(SURFACE, (0, 255, 0), (250, 250), coord0, 2)

        coord1 = pos1[0] * 25 + 250, pos1[1] * -25 + 250
        pygame.draw.line(SURFACE, (0, 255, 255), (250, 250), coord1, 2)

        pygame.draw.rect(SURFACE, (255, 255, 255), (0, 500, 500, 200))
        len0 = hypot(pos0[0], pos0[1])
        len1 = hypot(pos1[0], pos1[1])
        len2 = len0 * len1
        if len2 == 0:
            len2 = 0.000001

        strings = [
            "V1=({},{})".format(pos0[0], pos0[1]),
            "V2=({},{})".format(pos1[0], pos1[1]),
            "cross of V1 & V2={}".format(cross(pos0, pos1)),
            "|V1|={}".format(len0),
            "|V2|={}".format(len1),
            "sin(theta)={}".format(cross(pos0, pos1) / len2),
            "theta={}".format(degrees(asin(cross(pos0, pos1) / len2)))
        ]
        for index, bitmap_str in enumerate(strings):
            bmp = sys_font.render(bitmap_str, True, (0, 0, 0))
            SURFACE.blit(bmp, (20, index * 25 + 510))
        pygame.display.update()
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
