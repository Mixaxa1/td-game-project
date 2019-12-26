import sys

import pygame as pg

from Board import Board
from GUI import Gui

pg.init()
size = width, height = 500, 500
screen = pg.display.set_mode(size)


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = width
        self.screen_height = height

        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.running = False

        self.board_surface = pg.Surface((500, 500))
        self.gui_surface = pg.Surface((500, 50))

        self.load_level()

    def generate_level(self, size):
        x, y = size

        field = [['g'] * x] * y

        return field

    def load_level(self):
        field = [['g', 'g', 'g', 'g', 't1', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 's', 's', 's', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 'g', 'g', 's', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 's', 'g', 's', 's', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 's', 'g', 'g', 's', 'g', 't1', 'g', 'g'],
                 ['g', 't1', 's', 'g', 'g', 's', 'g', 's', 's', 's'],
                 ['s', 's', 's', 'g', 'g', 's', 'g', 's', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 's', 's', 's', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]

        # field = self.generate_level((10, 10))

        width, height = len(field), len(field[0])
        self.board = Board(width, height, field)

    def start(self):
        self.running = True
        self.run()

    def run(self):
        self.gui = Gui(width, height)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False


            self.screen.fill(pg.Color(0, 0, 0))

            self.board.draw(self.board_surface)
            self.screen.blit(self.board_surface, (0, 50))

            self.gui.draw(self.gui_surface)
            self.screen.blit(self.gui_surface, (0, 0))

            pg.display.flip()

    def terminate(self):
        pg.quit()
        sys.exit()