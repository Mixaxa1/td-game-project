import pygame as pg

from Tile import GrassTile, SandTile
from buildings import Base
from enemies import create_wave


class Board:
    def __init__(self, width, height, field):
        self.width = width
        self.height = height
        self.field = [row.copy() for row in field]

        self.surface = pg.Surface((500, 500))

        self.tiles_group = pg.sprite.Group()
        self.buildings_group = pg.sprite.Group()
        self.towers_group = pg.sprite.Group()
        self.enemies_group = pg.sprite.Group()

        self.grass = []
        self.sand = []
        self.enemies = []
        self.buildings = []
        self.towers = []

        self.base = None

        for row in range(len(field)):
            for col in range(len(field[row])):
                if field[row][col] == 'g':
                    self.add_grass((col, row))
                elif field[row][col] == 's':
                    self.add_sand((col, row))
                elif field[row][col] == 'sb':
                    self.add_sand((col, row))
                    base = Base(col, row, (self.buildings_group,), 50, 50)
                    self.add_base(base, [col, row])

        self.start = self.field[6][0].pos_x, self.field[6][0].pos_y
        self.path = [self.field[6][2], self.field[3][2], self.field[3][1], self.field[1][1], self.field[1][4],
                     self.field[3][4], self.field[3][5], self.field[7][5], self.field[7][7], self.field[5][7],
                     self.field[5][9]]

    def add_grass(self, cords):
        col, row = cords
        tile = GrassTile(col, row, (self.tiles_group,), 50, 50)
        self.field[row][col] = tile
        self.grass.append(tile)

    def add_sand(self, cords):
        col, row = cords
        tile = SandTile(col, row, (self.tiles_group,), 50, 50)
        self.field[row][col] = tile
        self.sand.append(tile)

    def add_base(self, base, cords):
        col, row = cords
        self.buildings.append(base)
        self.base = base
        self.field[row][col].built_up = True

    def add_tower(self, tower, cords):
        col, row = cords
        self.buildings.append(tower)
        self.towers.append(tower)
        self.field[row][col].built_up = True

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def start_new_wave(self, difficulty):
        self.enemies = create_wave(difficulty, self.start, self.path, self.enemies_group)

    def kill_enemy(self, enemy):
        enemy.kill()
        self.enemies.remove(enemy)

    def draw(self, surface):
        self.tiles_group.draw(surface)
        self.buildings_group.draw(surface)
        self.enemies_group.draw(surface)