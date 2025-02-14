import pygame as pg

from utils import load_image


class Tile(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(*groups)
        self.pos_x = pos_x * tile_width
        self.pos_y = pos_y * tile_height
        self.width = tile_width
        self.height = tile_height

        self.image = image
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class GrassTile(Tile):
    for_towers = True
    for_traps = False
    for_enemies = False

    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/grass1.jpg', (50, 50))
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)

        self.built_up = False


class SandTile(Tile):
    for_towers = False
    for_traps = True
    for_enemies = True

    def __init__(self, pos_x, pos_y, groups, tile_width, tile_height):
        self.image = load_image('images/sand3.jpg', (50, 50))
        super().__init__(self.image, pos_x, pos_y, groups, tile_width, tile_height)

        self.built_up = False
        self.enemy_on_tile = False
