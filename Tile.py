import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, groups, tile_width, tile_height):
        super().__init__(*groups)
        self.current_x = pos_x * tile_width
        self.current_y = pos_y * tile_height
        self.width = tile_width
        self.height = tile_height

        self.image = image
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect().move(self.current_x, self.current_y)