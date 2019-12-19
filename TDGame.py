import sys

import pygame as pg

from Board import Board

pg.init()
size = width, height = 500, 400
screen = pg.display.set_mode(size)


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = width
        self.screen_height = height

        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.running = False

        self.load_level()

    def load_level(self):
        field = [['g', 'g', 'g', 'g', 'g', 'g', 'g'], ['g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g'], ['g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g'], ['g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g'], ['g', 'g', 'g', 'g', 'g', 'g', 'g']]

        width, height = len(field), len(field[0])

        self.board = Board(width, height, field)

    def start(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.screen.fill(pg.Color(0, 0, 0))
            self.board.draw(self.screen)

            pg.display.flip()

    def terminate(self):
        pg.quit()
        sys.exit()