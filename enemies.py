import random

import pygame as pg
from utils import load_image


class Enemy(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, path, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.path = path

        self.x_count = 0
        self.y_count = 0
        self.on_finish = False

        self.create_time = 0
        self.delay = 0

        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def find_target_location(self):
        if not self.path:
            self.on_finish = True
        else:
            self.x_count = (self.path[0].pos_x + 10 - self.pos_x) / self.speed
            self.y_count = (self.path[0].pos_y + 10 - self.pos_y) / self.speed

            self.path.pop(0)

    def step(self):
        if self.x_count == 0 and self.y_count == 0:
            self.find_target_location()

        if self.x_count > 0:
            self.pos_x += self.speed
            self.x_count -= 1
        elif self.x_count < 0:
            self.pos_x -= self.speed
            self.x_count += 1

        if self.y_count > 0:
            self.pos_y += self.speed
            self.y_count -= 1
        elif self.y_count < 0:
            self.pos_y -= self.speed
            self.y_count += 1

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y


class Goblin(Enemy):
    cost = 1

    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/goblin.png', (30, 30), -1)
        self.hp = 5
        self.dmg = 1
        self.speed = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Hobgoblin(Enemy):
    cost = 2

    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/hobgoblin.png', (30, 30), -1)
        self.hp = 15
        self.dmg = 1
        self.speed = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Mercenary(Enemy):
    cost = 5

    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/mercenary.png', (30, 30), -1)
        self.hp = 20
        self.dmg = 2
        self.speed = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Orc(Enemy):
    cost = 10

    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/orc.png', (30, 30), -1)
        self.hp = 45
        self.dmg = 5
        self.speed = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Wizard(Enemy):
    cost = 30

    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/wizard.png', (30, 30), -1)
        self.hp = 70
        self.dmg = 10
        self.speed = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


def create_wave(difficulty, start, path, groups):
    start = start[0] + 10, start[1] + 10
    possible_enemies = [Goblin(*start, path, groups), Hobgoblin(*start, path, groups),
                        Mercenary(*start, path, groups), Orc(*start, path, groups), Wizard(*start, path, groups)]
    possible_enemies = [possible_enemies[i] for i in range(len(possible_enemies)) if i <= difficulty - 1]

    budget = difficulty * 10
    wave = []

    while budget != 0:
        enemy = random.choice(possible_enemies)

        if enemy.cost <= budget:
            budget -= enemy.cost
            wave.append(enemy)

    return wave