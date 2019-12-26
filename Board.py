import pygame as pg

from Tile import GrassTile, SandTile
from buildings import TowerTest
from enemies import EnemyTest


class Board:
    def __init__(self, width, height, field):
        self.width = width
        self.height = height
        self.field = [row.copy() for row in field]

        self.tiles_group = pg.sprite.Group()
        self.enemies_group = pg.sprite.Group()

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
                    tower = TowerTest(col, row, (self.tiles_group,), 50, 50)
                    self.add_tower(tower, [col, row])
                if field[row][col] == 'e':
                    self.add_enemy(EnemyTest(5, 5, col, row, self.enemies_group))

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
        y, x = cords
        if self.field[x][y].for_towers and not self.field[x][y].built_up:
            self.buildings.append([tower, cords])
            self.field[x][y].built_up = True
        else:
            print('Это место уже занято или не пригодно для строительсва башни')

    def add_trap(self, trap, cords):
        y, x = cords
        if self.field[x][y].for_traps and not self.field[x][y].built_up:
            self.buildings.append([trap, cords])
            self.field[x][y].built_up = True
        else:
            print('Это место уже занято или не пригодно для строительсва ловушки')

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def draw(self, screen):
        self.tiles_group.draw(screen)