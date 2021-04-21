from math import pi
import math
import pygame as pg
import random
import time


boids = []
boids_sprite = []
width = 700
height = 700
boids_number = 50


class boid_sprite(pg.sprite.Sprite):
    def __init__(self, boid):
        super().__init__()
        self.boid = boid
        self.image = pg.Surface((6, 10))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.polygon(self.image, (75, 75, 255), [(0, 0), (10, 6 / 2), (0, 6)])
        self.rect = self.image.get_rect()

    def update(self):
        self.boid.update()
        self.rect.x = self.boid.pos[0]
        self.rect.y = self.boid.pos[1]


class single_boid:
    def __init__(
        self,
        radius=60,
        blankangle=pi / 6,
        reactivity=20,
        max_force=5,
        magnitude1=0.05,
        magnitude2=10,
        magnitude3=10,
        x=0,
        y=0,
        angle=1,
    ):
        """Initiate the boid object with setted position, angle, and vision range"""
        global boids
        boids.append(self)
        self.pos = Vector2((x, y))
        self.velocity = Vector2((0, 0))
        self.angle = angle  # set the angle of the boid
        # set the blank angle
        self.blankangle = blankangle
        # here we set the "reactivity" of the boid. If distance is less than this, it reacts
        self.reactivity = reactivity
        self.range = radius
        self.max_force = max_force
        self.magnitude1 = magnitude1
        self.magnitude2 = magnitude2
        self.magnitude3 = magnitude3

    def get_farness(self, boid):
        return (
            (self.pos[0] - boid.pos[0]) ** 2 + (self.pos[1] - boid.pos[1]) ** 2
        ) ** 0.5

    def minimize(self, value):
        if value[0] != self.max_force and value[1] != self.max_force:
            return value
        if value[0] == value[1]:
            value.values[0], value.values[1] = self.max_force, self.max_force
            return value
        highest = max(value[0], value[1])
        lowest = min(value[0], value[1])
        ratio = min(value[0], value[1]) / highest
        highest = value.values.index(highest)
        lowest = value.values.index(lowest)
        value.values[highest] = self.max_force
        value.values[lowest] = ratio * self.max_force
        return value

    def get_neighbors(self):
        neighbors = []
        for boid in boids:
            if (
                self.get_farness(boid) < self.range
                and boid != self
                and not pi + self.angle + self.blankangle
                < self.pos.angle_between(boid.pos)
                < self.angle + pi - self.blankangle
            ):
                neighbors.append(boid)
        return neighbors

    def rule0(self):
        velocity = Vector2((0, 0))
        velocity.values[0] = math.cos(self.angle) * self.max_force
        velocity.values[1] = math.sin(self.angle) * self.max_force
        return velocity

    def rule1(self):
        velocity = Vector2((0, 0))
        boids = self.get_neighbors()
        if not boids:
            return velocity
        for boid in boids:
            if self.get_farness(boid) < self.reactivity:
                velocity = velocity - (self.pos - boid.pos)
        velocity = self.minimize(velocity)
        return velocity * self.magnitude1

    def rule2(self):
        velocity = Vector2((0, 0))
        boids = self.get_neighbors()
        if not boids:
            return velocity
        for boid in boids:
            velocity = velocity + boid.velocity
        velocity = (velocity * (1 / len(boids))) - self.velocity
        velocity = self.minimize(velocity)
        return velocity * self.magnitude2

    def rule3(self):
        velocity = Vector2((0, 0))
        boids = self.get_neighbors()
        if not boids:
            return velocity
        for boid in boids:
            velocity = velocity + boid.pos
        velocity = (velocity * (1 / len(boids))) - self.pos
        velocity = self.minimize(velocity)
        return velocity * self.magnitude3

    def update(self):
        vel0 = self.rule0()
        vel1 = self.minimize(self.rule1())
        vel2 = self.minimize(self.rule2())
        vel3 = self.minimize(self.rule3())
        self.velocity = vel0 + vel1
        self.velocity = self.velocity + vel2
        self.velocity = self.velocity + vel3
        # print(self.velocity.values)
        pos = self.pos + self.velocity
        """self.angle = self.pos.angle_between(pos) % (pi * 2)
        self.angle += random.choice((random.random()
                                     * 2, -random.random() * 2))"""

        self.pos = pos
        if self.pos.values[0] > width:
            self.pos.values[0] = 1
        if self.pos.values[0] < 1:
            self.pos.values[0] = width
        if self.pos.values[1] > height:
            self.pos.values[1] = 1
        if self.pos.values[1] < 1:
            self.pos.values[0] = height


class Vector2:
    def __init__(self, values):
        self.values = list(values)

    def __add__(self, value):
        return Vector2((self[0] + value[0], self[1] + value[1]))

    def __sub__(self, value):
        return Vector2((self[0] - value[0], self[1] + value[1]))

    def __mul__(self, value):
        if not isinstance(value, Vector2):
            return Vector2((self[0] * value, self[1] * value))
        else:
            return self.dot(self.values, value.values)

    @staticmethod
    def dot(a, b):
        return sum(i * j for i, j in zip(a, b))

    @staticmethod
    def magnitude(x, y):
        return math.sqrt((x ** 2) + (y ** 2))

    def angle_between(self, vector):
        return math.acos(
            (
                self.dot(self.values, vector.values)
                % (pi * 2)
                / ((self.magnitude(*self.values) * self.magnitude(*vector.values)))
            )
        )

    def __getitem__(self, other):
        return self.values[other]


def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Boids")
    loop = True
    clock = pg.time.Clock()
    all_sprites_list = pg.sprite.Group()
    for i in range(boids_number):
        boid = boid_sprite(
            single_boid(
                x=random.randint(1, height),
                y=random.randint(1, width),
                angle=random.random() * 360,
            ),
        )
        all_sprites_list.add(boid)
        boids_sprite.append(boid)

    while loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
        for boid in boids_sprite:
            # print(boids_sprite.index(boid))
            boid.update()
        all_sprites_list.update()
        screen.fill((255, 255, 255))
        all_sprites_list.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()


main()
