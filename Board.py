from Tile import Tile
from utils import load_image
import pygame as pg


class Board:
    def __init__(self, width, height, field):
        self.grass_image = load_image('images/grass1.jpg')

        self.width = width
        self.height = height
        self.field = [row.copy() for row in field]

        self.tiles_group = pg.sprite.Group()

        self.grass = []
        self.sand = []

        self.enemies = []
        self.buildings = []

        for row in range(len(field)):
            for col in range(len(field[row])):
                if field[row][col] == 'g':
                    self.grass.append(Tile(self.grass_image, col, row, (self.tiles_group,), 50, 50))


    def draw(self, screen):
        self.tiles_group.draw(screen)