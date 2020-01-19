from math import sqrt

import pygame as pg

from utils import load_image


class Buildings(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(*groups)
        self.pos_x = pos_x * tile_width
        self.pos_y = pos_y * tile_height
        self.width = tile_width
        self.height = tile_height

        self.time_adjustment = 0
        self.last_shot_time = 0

        self.image = image
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Base(Buildings):
    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/base.png', (tile_width, tile_height), -1)
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)


class Towers(Buildings):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(image, pos_x, pos_y, groups, tile_width, tile_height)

    def shot(self, enemy):
        enemy.hp -= self.dmg

    def determine_distance(self, enemy):
        tower_cords = self.pos_x + 25, self.pos_y + 25
        enemy_cords = enemy.pos_x + 15, enemy.pos_y + 15

        cord_difference = abs(tower_cords[0] - enemy_cords[0]), abs(tower_cords[1] - enemy_cords[1])
        distance = sqrt(cord_difference[0] ** 2 + cord_difference[1] ** 2)

        return distance


class ArcherTower(Towers):
    dmg = 5
    reload_time = 0.5
    attack_range = 100
    cost = 15

    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/ArcherTower.jpg', (tile_width, tile_height), -1)
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)


class BallisticTower(Towers):
    dmg = 10
    reload_time = 1
    attack_range = 125
    cost = 20

    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/BallisticTower.jpg', (tile_width, tile_height), -1)
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)


class MagicTower(Towers):
    dmg = 20
    reload_time = 1.5
    attack_range = 150
    cost = 25

    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/MagicTower.jpg', (tile_width, tile_height), -1)
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)


def buildings_factory(name, pos_x, pos_y, groups, tile_width, tile_height):
    if name == "ArcherTower":
        return ArcherTower(pos_x, pos_y, groups, tile_width, tile_height)
    elif name == "BallisticTower":
        return BallisticTower(pos_x, pos_y, groups, tile_width, tile_height)
    elif name == "MagicTower":
        return MagicTower(pos_x, pos_y, groups, tile_width, tile_height)