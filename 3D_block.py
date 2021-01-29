import sys
import random
from math import sin, cos, floor, radians
import pygame
from pygame.locals import QUIT, K_LEFT, K_RIGHT, KEYDOWN

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode([600, 600])
FPS_CLOCK = pygame.time.Clock()


class Cube:
    """ Cube for blocks and paddle """
    polygons = [
        [2, 1, 5, 6], [0, 1, 2, 3], [4, 5, 1, 0],
        [2, 6, 7, 3], [7, 6, 5, 4], [0, 3, 7, 4]
    ]

    def __init__(self, x, y, z, w, h, d, color):
        self.pos_x = x
        self.pos_y = y
        self.width = w
        self.height = h
        self.color = color
        self.pos = []
        self.vertices = [
            {"x": x - w, "y": y - h, "z": z + d},
            {"x": x - w, "y": y + h, "z": z + d},
            {"x": x + w, "y": y + h, "z": z + d},
            {"x": x + w, "y": y - h, "z": z + d},
            {"x": x - w, "y": y - h, "z": z - d},
            {"x": x - w, "y": y + h, "z": z - d},
            {"x": x + w, "y": y + h, "z": z - d},
            {"x": x + w, "y": y - h, "z": z - d}
        ]

    def set_camera(self, rad_x, rad_y):
        """update vertices positions depending on camera location"""
        self.pos.clear()
        for vert in self.vertices:
            p0x = vert["x"]
            p0y = vert["y"]
            p0z = vert["z"]

            # rotate around X axis
            p1x = p0x
            p1y = p0y * cos(rad_x) - p0z * sin(rad_x)
            p1z = p0y * sin(rad_x) + p0z * cos(rad_x)

            # rotate around Y axis
            p2x = p1x * cos(rad_y) + p1z * sin(rad_y)
            p2y = p1y
            p2z = -p1x * sin(rad_y) + p1z * cos(rad_y)

            self.pos.append({"x": p2x, "y": p2y, "z": p2z})

    def is_hit(self, pos_x, pos_y):
        """return if (x,y) hits the block"""
        return self.pos_x - self.width < pos_x < self.pos_x + self.width \
               and self.pos_y - self.height < pos_y < self.pos_y + self.height

    def translate(self, diff_x, diff_y):
        """move the block"""
        self.pos_x += diff_x
        self.pos_y += diff_y
        for vert in self.vertices:
            vert["x"] += diff_x
            vert["y"] += diff_y


def tick():
    """called periodically from the main loop"""
    global SPEED, THETA, BLOCKS, MESSAGE
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.translate(-10, 0)
            elif event.key == K_RIGHT:
                PADDLE.translate(+10, 0)

    if MESSAGE is not None:
        return

    # move the ball
    diff_x = cos(radians(THETA)) * SPEED
    diff_y = sin(radians(THETA)) * SPEED
    BALL.translate(diff_x, diff_y)

    # hit any blocks?
    count = len(BLOCKS)
    BLOCKS = [x for x in BLOCKS if x == BALL or x == PADDLE or not x.is_hit(BALL.pos_x, BALL.pos_y)]

    if len(BLOCKS) != count:
        THETA = -THETA

    if BALL.pos_y > 800:
        THETA = -THETA
        SPEED = 10

    if BALL.pos_x < -250 or BALL.pos_x > 250:
        THETA = 180 - THETA

    if PADDLE.is_hit(BALL.pos_x, BALL.pos_y):
        THETA = 90 + ((PADDLE.pos_x - BALL.pos_x) / PADDLE.width) * 80

    if BALL.pos_y < -1200 and len(BLOCKS) > 2:
        MESSAGE = MESS1

    if len(BLOCKS) == 2:
        MESSAGE = MESS0

    # Rotate the Cube
    rad_y = PADDLE.pos_x / 1000
    rad_x = 0.5 + BALL.pos_y / 2000
    for block in BLOCKS:
        block.set_camera(rad_x, rad_y)


def paint():
    """update the screen"""
    SURFACE.fill((0, 0, 0))

    for block in BLOCKS:
        for indices in block.polygons:
            poly = []
            for index in indices:
                pos = block.pos[index]
                pos_z = pos["z"] + 500
                pos_x = pos["x"] * 500 / pos_z + 300
                pos_y = -pos["y"] * 500 / pos_z + 500
                poly.append((pos_x, pos_y))
            pygame.draw.lines(SURFACE, block.color, True, poly)

    if MESSAGE is not None:
        SURFACE.blit(MESSAGE, (150, 400))

    pygame.display.update()


FPS = 40
SPEED = 5
THETA = 270 + floor(random.randint(-10, 10))
BLOCKS = []
BALL = Cube(0, 400, 0, 5, 5, 5, (255, 255, 0))
PADDLE = Cube(0, 0, 0, 30, 10, 5, (255, 255, 255))
MESSAGE = None
MY_FONT = pygame.font.SysFont(None, 80)
MESS0 = MY_FONT.render("Cleared!!!", True, (255, 255, 0))
MESS1 = MY_FONT.render("Game Over!", True, (255, 255, 0))


def main():
    """main routine"""
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0), (0, 128, 0), (128, 0, 128), (0, 0, 250)]

    for pos_y in range(0, len(colors)):
        for pos_x in range(-3, 4):
            block = Cube(pos_x * 70, pos_y * 50 + 450, 0, 30, 10, 5, colors[pos_y])
            BLOCKS.append(block)

    BLOCKS.append(PADDLE)
    BLOCKS.append(BALL)

    while True:
        tick()
        paint()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
