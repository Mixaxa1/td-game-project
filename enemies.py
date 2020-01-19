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
            self.x_count = (self.path[0].pos_x + 10 - self.pos_x) // self.speed
            self.y_count = (self.path[0].pos_y + 10 - self.pos_y) // self.speed

            self.path.pop(0)

    def step(self, speed_up):

        if self.x_count == 0 and self.y_count == 0:
            self.find_target_location()

        if self.create_time >= self.delay:
            if speed_up == 2 and self.x_count == 1 or self.y_count == 1:
                speed_up = 1
            if self.x_count > 0:
                self.pos_x += self.speed * speed_up
                self.x_count -= 1 * speed_up
            elif self.x_count < 0:
                self.pos_x -= self.speed * speed_up
                self.x_count += 1 * speed_up

            if self.y_count > 0:
                self.pos_y += self.speed * speed_up
                self.y_count -= 1 * speed_up
            elif self.y_count < 0:
                self.pos_y -= self.speed * speed_up
                self.y_count += 1 * speed_up

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
        else:
            self.create_time += 1 * speed_up


class Goblin(Enemy):
    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/goblin.png', (30, 30), -1)
        self.hp = 5
        self.dmg = 1
        self.speed = 1
        self.reward = 1
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Hobgoblin(Enemy):
    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/hobgoblin.png', (30, 30), -1)
        self.hp = 15
        self.dmg = 1
        self.speed = 0.85
        self.reward = 2
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Mercenary(Enemy):
    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/mercenary.png', (30, 30), -1)
        self.hp = 20
        self.dmg = 2
        self.speed = 0.75
        self.reward = 3
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Orc(Enemy):
    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/orc.png', (30, 30), -1)
        self.hp = 45
        self.dmg = 5
        self.speed = 0.60
        self.reward = 3
        super().__init__(self.image, pos_x, pos_y, path, groups)


class Wizard(Enemy):
    def __init__(self, pos_x, pos_y, path, groups):
        self.image = load_image('images/wizard.png', (30, 30), -1)
        self.hp = 70
        self.dmg = 10
        self.speed = 0.55
        self.reward = 10
        super().__init__(self.image, pos_x, pos_y, path, groups)


def create_wave(difficulty, start, path, groups):
    possible_enemies = ['Goblin', 'Hobgoblin', 'Mercenary', 'Orc', 'Wizard']
    possible_enemies = [possible_enemies[i] for i in range(len(possible_enemies)) if i <= difficulty - 1]

    budget = difficulty * 10
    wave = []
    prices = {'Goblin': 1, 'Hobgoblin': 2, 'Mercenary': 5, 'Orc': 10, 'Wizard': 30}

    while budget != 0:
        enemy = random.choice(possible_enemies)

        if prices[enemy] <= budget:
            budget -= prices[enemy]
            wave.append(enemy)

    start = start[0] + 10 - 50, start[1] + 10
    delay = 0

    for i in range(len(wave)):
        wave[i] = enemies_factory(wave[i], *start, path, groups)
        wave[i].delay = delay

        delay += 25

    return wave


def enemies_factory(name, pos_x, pos_y, path, groups):
    if name == "Goblin":
        return Goblin(pos_x, pos_y, path[:], groups)
    elif name == "Hobgoblin":
        return Hobgoblin(pos_x, pos_y, path[:], groups)
    elif name == "Mercenary":
        return Mercenary(pos_x, pos_y, path[:], groups)
    elif name == "Orc":
        return Orc(pos_x, pos_y, path[:], groups)
    elif name == "Wizard":
        return Wizard(pos_x, pos_y, path[:], groups)