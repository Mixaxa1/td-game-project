import pygame as pg

from Tile import GrassTile, SandTile
from buildings import TowerTest, buildings_factory


class Board:
    def __init__(self, width, height, field):
        self.width = width
        self.height = height
        self.field = [row.copy() for row in field]

        self.surface = pg.Surface((500, 500))

        self.tiles_group = pg.sprite.Group()
        self.buildings_group = pg.sprite.Group()

        self.grass = []
        self.sand = []

        self.enemies = []
        self.buildings = []

        for row in range(len(field)):
            for col in range(len(field[row])):
                if field[row][col] == 'g':
                    self.add_grass((col, row))
                if field[row][col] == 's':
                    self.add_sand((col, row))
                if field[row][col] == 't1':
                    self.add_grass((col, row))
                    tower = TowerTest(col, row, (self.buildings_group,), 50, 50)
                    self.add_tower(tower, [col, row])

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

    def add_tower(self, tower, cords):
        col, row = cords
        if self.field[row][col].for_towers and not self.field[row][col].built_up and type(tower) == str:
            tower = buildings_factory(tower, cords[0], cords[1], (self.buildings_group,), 50, 50)
            self.buildings.append(tower)
            self.field[row][col].built_up = True
        else:
            print('Это место уже занято или не пригодно для строительсва башни')

    def add_trap(self, trap, cords):
        col, row = cords
        if self.field[row][col].for_traps and not self.field[row][col].built_up:
            self.buildings.append(trap)
            self.field[row][col].built_up = True
        else:
            print('Это место уже занято или не пригодно для строительсва ловушки')

    def add_enemy(self, enemy, cords):
        self.enemies.append(enemy)
        self.enemy.cord = cords

    def draw(self, surface):
        self.tiles_group.draw(surface)
        self.buildings_group.draw(surface)