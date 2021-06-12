import math
import pygame as pg
import numpy as np
import random as r

boids = []
boids_sprites = []
max_movement = 20
radius = 50
view_angle = 230
how_many = 20

WIDTH = 800
HEIGHT = 800

factors = (3, 1, 1)

neutral_angle = pg.Vector2(0, 1)


class Boid:
    def __init__(
        self,
        pos=None,
        velocity=None,
    ):
        if not pos:
            pos = pg.Vector2(r.randint(0, WIDTH), r.randint(0, HEIGHT))

        if not velocity:
            velocity = pg.Vector2(r.randint(0, WIDTH), r.randint(0, HEIGHT))

        self.pos = pos
        self.velocity = velocity
        self.angle = 0
        boids.append(self)

    def get_neighbours(self):
        for boid in boids:
            if self != boid:
                if self.distance_to_point(boid) < radius:
                    if (
                        view_angle
                        > boid.velocity.angle_to(boid.pos - self.pos)
                        > -view_angle
                    ):
                        yield boid

    def limit(self):
        x, y = self.velocity[0], self.velocity[1]
        largest = max(x, y)
        x, y = (x / largest) * max_movement, (y / largest) * max_movement
        self.velocity = pg.Vector2(x, y)

    def average_position(self):
        neighbours = list(self.get_neighbours())
        average_pos = pg.Vector2()
        if len(neighbours):
            for neighbour in neighbours:
                average_pos += neighbour.pos - self.pos
            average_pos /= len(neighbours)
        return average_pos

    def average_velocity(self):
        neighbours = list(self.get_neighbours())
        average_vel = pg.Vector2()
        if len(neighbours):
            for neighbour in neighbours:
                average_vel += neighbour.velocity - self.velocity
            average_vel /= len(neighbours)
        return average_vel

    def distance_to_point(self, boid):
        return (
            abs(self.pos[0] - boid.pos[0]) ** 2 + abs(self.pos[1] - boid.pos[1]) ** 2
        ) ** 0.5

    def rule1(self):
        neighbours = list(self.get_neighbours())
        steering = pg.Vector2()
        if len(neighbours):
            for neighbour in neighbours:
                distance = self.distance_to_point(neighbour)
                if distance != 0:
                    steering += (neighbour.pos - self.pos) / distance
            steering /= len(neighbours)
        self.velocity += steering * factors[0]

    def rule2(self):
        average_vel = self.average_velocity() - self.velocity
        self.velocity += average_vel * factors[1]

    def rule3(self):
        average_pos = self.average_position() - self.pos
        self.velocity += average_pos * factors[2]

    def update(self):
        self.rule1()
        self.rule2()
        self.rule3()
        self.limit()
        self.pos += self.velocity
        self.angle = neutral_angle.angle_to(self.velocity)

        if self.pos[1] > HEIGHT:
            self.pos[1] = 0

        if self.pos[0] > WIDTH:
            self.pos[0] = 0

        if self.pos[1] < 0:
            self.pos[1] = HEIGHT

        if self.pos[0] < 0:
            self.pos[0] = WIDTH


class boid_sprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        boids_sprites.append(self)
        self.boid = Boid()
        self.image = pg.Surface((6, 10))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.polygon(self.image, (75, 75, 255), [(0, 0), (20, 12 / 2), (0, 12)])
        self.rect = self.image.get_rect()

    def update(self):
        self.boid.update()
        self.rect.x = self.boid.pos[0]
        self.rect.y = self.boid.pos[1]
        # self.image


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Boids")
    loop = True
    clock = pg.time.Clock()
    all_sprites_list = pg.sprite.Group()
    for _ in range(how_many):
        boid = boid_sprite()
        all_sprites_list.add(boid)
    finished = False
    while not finished:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        for boid in boids_sprites:
            boid.update()
        all_sprites_list.update()
        screen.fill((255, 255, 255))
        all_sprites_list.draw(screen)
        pg.display.flip()
        clock.tick(5)
    pg.quit()


main()
