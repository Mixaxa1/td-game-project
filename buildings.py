import pygame as pg

from utils import load_image


class Buildings(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(*groups)
        self.pos_x = pos_x * tile_width
        self.pos_y = pos_y * tile_height
        self.width = tile_width
        self.height = tile_height

        self.image = image
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Towers(Buildings):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(image, pos_x, pos_y, groups, tile_width, tile_height)


class TowerTest(Towers):
    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/tower1.jpg', (50, 50), -1)
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)


def buildings_factory(name, pos_x, pos_y, groups, tile_width, tile_height):
    if name == "tower1":
        return TowerTest(pos_x, pos_y, groups, tile_width, tile_height)