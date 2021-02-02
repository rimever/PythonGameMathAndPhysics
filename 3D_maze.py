import sys
import random
from math import sin, cos, pi, sqrt, floor
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE


def normalize(vector):
    """ normalize the vector(make the length 1)"""
    scale = 1 / sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    return vector[0] * scale, vector[1] * scale, vector[2] * scale


def get_norm_vector(pos1, pos2, pos3):
    """ get the normal vector from 3 vertices """
    pvec = (pos1[0] - pos2[0], pos1[1] - pos2[1], pos1[2] - pos2[2])
    qvec = (pos1[0] - pos3[0], pos1[1] - pos3[1], pos1[2] - pos3[2])
    norm = (
        pvec[1] * qvec[2] - pvec[2] * qvec[1], pvec[2] * qvec[0] - pvec[0] * qvec[2],
        pvec[0] * qvec[1] - pvec[1] * qvec[0])
    return normalize(norm)


def create_maze(width, height):
    """ create maze data (0:empty, 1:wall)"""
    maze = [[0 for i in range(width)] for j in range(height)]
    for pos_z in range(0, height):
        for pos_x in range(0, width):
            if pos_x in (0, width - 1) or pos_z in (0, height - 1):
                maze[pos_z][pos_x] = 1
            if pos_z % 2 == 1 or pos_x % 2 == 1:
                continue
            if 1 < pos_z < height - 1 and 1 < pos_x < width - 1:
                maze[pos_z][pos_x] = 1
                direction = random.randint(0, 3 if pos_z == 2 else 2)
                (next_x, next_z) = (pos_x, pos_z)
                if direction == 0:
                    next_z += 1
                elif direction == 1:
                    next_x -= 1
                elif direction == 2:
                    next_x += 1
                elif direction == 3:
                    next_z -= 1
                maze[next_z][next_x] = 1

    return maze


class Surface:
    """object for each surface"""

    def __init__(self, v0, v1, v2, v3, tag, index):
        self.vert = (v0, v1, v2, v3)
        self.tag = tag
        self.index = index
        self.norm = (0, 0, 0)
        self.pos_z = 0

    def update(self):
        """update the normal  vector of surface"""
        self.norm = get_norm_vector(self.vert[0], self.vert[1], self.vert[2])
        self.pos_z = (self.vert[0][2] + self.vert[1][2] + self.vert[2][2] + self.vert[3][2]) / 4
        if self.index == 0:
            self.pos_z -= 1


class Cube:
    """ 3D Cube model"""
    polygons = (
        (2, 1, 5, 6), (0, 1, 2, 3), (4, 5, 1, 0),
        (2, 6, 7, 3), (7, 6, 5, 4), (0, 3, 7, 4)
    )

    def __init__(self, x, y, z, w, h, d, tag):
        self.pos_x = x
        self.pos_z = z
        self.pos = []
        self.surfaces = []
        self.vertices = (
            (x - w, y - h, z + d),
            (x - w, y + h, z + d),
            (x + w, y + h, z + d),
            (x + w, y - h, z + d),
            (x - w, y - h, z - d),
            (x - w, y + h, z - d),
            (x + w, y + h, z - d),
            (x + w, y - h, z - d)
        )
        for vert in self.vertices:
            self.pos.append([vert[0], vert[1], vert[2]])

        for i in range(5):
            indices = self.polygons[i]
            pos0 = self.pos[indices[0]]
            pos1 = self.pos[indices[1]]
            pos2 = self.pos[indices[2]]
            pos3 = self.pos[indices[3]]
            self.surfaces.append(Surface(pos0, pos1, pos2, pos3, tag, i))

    def set_camera(self, camera_x, camera_y, camera_z, mrot_x, mrot_y):
        """set camera location and update vertices positions"""
        for i in range(len(self.vertices)):
            vert = self.vertices[i]
            pos_x = vert[0] - camera_x
            pos_y = vert[1] - camera_y
            pos_z = vert[2] - camera_z

            # rotate around Y axis
            ppos = mrot_y[0] * pos_x + mrot_y[1] * pos_y + mrot_y[2] * pos_z
            qpos = mrot_y[3] * pos_x + mrot_y[4] * pos_y + mrot_y[5] * pos_z
            rpos = mrot_y[6] * pos_x + mrot_y[7] * pos_y + mrot_y[8] * pos_z

            # rotate around X axis
            self.pos[i][0] = mrot_x[0] * ppos + mrot_x[1] * qpos + mrot_x[2] * rpos
            self.pos[i][1] = mrot_x[3] * ppos + mrot_x[4] * qpos + mrot_x[5] * rpos
            self.pos[i][2] = mrot_x[6] * ppos + mrot_x[7] * qpos + mrot_x[8] * rpos

        for surface in self.surfaces:
            surface.update()


pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
SURFACE.convert()
FPS_CLOCK = pygame.time.Clock()
(W, H) = (13, 13)
XPOS = [1, 1]
ZPOS = [1, 1]
TURN = [1, 1]
COUNTER = 0
CAMERAY = 50
JUMP_SPEED = 0
LIGHT = normalize([0.5, -0.8, -0.2])
FPS = 30
CUBES = []
MAZE = create_maze(W, H)


def event_loop():
    """handle events in event_loop"""
    global COUNTER, JUMP_SPEED, CUBES
    (diff_x, diff_z) = (0, 0)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                TURN[1] = TURN[0] + 1
            elif event.key == K_RIGHT:
                TURN[1] = TURN[0] - 1
            elif event.key == K_UP:
                diff_x = round(cos(TURN[0] * pi / 2))
                diff_z = round(sin(TURN[0] * pi / 2))
            elif event.key == K_DOWN:
                diff_x = -round(cos(TURN[0] * pi / 2))
                diff_z = -round(sin(TURN[0] * pi / 2))
            elif event.key == K_SPACE and JUMP_SPEED == 0:
                JUMP_SPEED = 150

        if COUNTER != 0:
            continue

        if not (diff_x == 0 and diff_z == 0) and (MAZE[ZPOS[0] + diff_z][XPOS[0] + diff_x] == 0):
            CUBES = [c for c in CUBES if not (c.pos_x / 100 == XPOS[0] + diff_x and c.pos_z / 100 == ZPOS[0] + diff_z)]
            CUBES = [c for c in CUBES if
                     not (c.pos_x / 100 == XPOS[0] + diff_x * 2 and c.pos_z / 100 == ZPOS[0] + diff_z * 2)]
            (XPOS[1], ZPOS[1]) = (XPOS[0] + diff_x * 2, ZPOS[0] + diff_z * 2)

        if TURN[1] != TURN[0] or XPOS[1] != XPOS[0] or ZPOS[1] != ZPOS[0]:
            COUNTER = 1


def tick():
    """called periodically from the main loop"""
    global COUNTER, CAMERAY, JUMP_SPEED
    event_loop()

    camera_rot_y = TURN[0] * pi / 2 - pi / 2
    (camera_x, camera_z) = (XPOS[0] * 100, ZPOS[0] * 100)
    if COUNTER > 0:
        camera_rot_y += ((TURN[1] - TURN[0]) * COUNTER / 10) * (pi / 2)
        camera_x += ((XPOS[1] - XPOS[0]) * COUNTER / 10) * 100
        camera_z += ((ZPOS[1] - ZPOS[0]) * COUNTER / 10) * 100
        COUNTER += 1
        if COUNTER >= 10:
            TURN[0] = TURN[1] = (TURN[1] + 4) % 4
            (XPOS[0], ZPOS[0]) = (XPOS[1], ZPOS[1])
            COUNTER = 0

    JUMP_SPEED -= 4
    CAMERAY += JUMP_SPEED
    if CAMERAY < 50:
        JUMP_SPEED = 0
        CAMERAY = 50

    (cval, sval) = (cos(camera_rot_y), sin(camera_rot_y))
    mrot_y = [cval, 0, sval, 0, 1, 0, -sval, 0, cval]
    mrot_x = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    if CAMERAY != 50:
        camera_rot_x = min(90, (CAMERAY - 50) / 20) * pi / 180
        (cval, sval) = (cos(-camera_rot_x), sin(-camera_rot_x))
        mrot_x = [1, 0, 0, 0, cval, -sval, 0, sval, cval]
    for cube in CUBES:
        cube.set_camera(camera_x, CAMERAY, camera_z, mrot_x, mrot_y)


def paint():
    """update the surface"""
    SURFACE.fill((0, 0, 0))
    surfaces = []
    for cube in CUBES:
        surfaces.extend(cube.surfaces)

    surfaces = sorted(surfaces, key=lambda x: x.pos_z, reverse=True)

    for surface in surfaces:
        dot = surface.norm[0] * LIGHT[0] + surface.norm[1] * LIGHT[1] + surface.norm[2] * LIGHT[2]
        ratio = (dot + 1) / 2
        (rval, gval, bval) = (0, 255, 128) if surface.tag == "dot" else (255, 255, 255)
        (rval, gval, bval) = (floor(rval * ratio), floor(gval * ratio), floor(bval * ratio))

        pts = []
        for i in range(4):
            (pos_x, pos_y, pos_z) = (surface.vert[i][0], surface.vert[i][1], surface.vert[i][2])
            if pos_z <= 10:
                continue
            pos_x = int(pos_x * 1000 / pos_z + 300)
            pos_y = int(-pos_y * 1000 / pos_z + 300)
            pts.append((pos_x, pos_y))

        if len(pts) > 3:
            pygame.draw.polygon(SURFACE, (rval, gval, bval), pts)

    pygame.display.update()


def main():
    """main routine"""
    for pos_z in range(0, H):
        for pos_x in range(0, W):
            if MAZE[pos_z][pos_x] == 1:
                CUBES.append(Cube(pos_x * 100 - 25, 0, pos_z * 100 - 25, 25, 25, 25, "wall"))
                CUBES.append(Cube(pos_x * 100 + 25, 0, pos_z * 100 - 25, 25, 25, 25, "wall"))
                CUBES.append(Cube(pos_x * 100 - 25, 0, pos_z * 100 + 25, 25, 25, 25, "wall"))
                CUBES.append(Cube(pos_x * 100 + 25, 0, pos_z * 100 + 25, 25, 25, 25, "wall"))
            else:
                CUBES.append(Cube(pos_x * 100, 0, pos_z * 100, 10, 10, 10, "dot"))

    while True:
        tick()
        paint()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
