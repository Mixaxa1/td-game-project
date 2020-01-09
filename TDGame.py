import sys

import pygame as pg

from Board import Board
from GUI import Gui
import buildings

pg.init()
size = width, height = 500, 550
screen = pg.display.set_mode(size)


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = width
        self.screen_height = height

        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.running = False
        self.pause = True
        self.speed_up = False

        self.board_surface = pg.Surface((500, 500))
        self.gui_surface = pg.Surface((500, 50))

        self.load_level()

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

        width, height = len(field), len(field[0])
        self.board = Board(width, height, field)

    def start(self):
        self.running = True
        self.run()

    def pause_continue(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True

    def speed_up_on_off(self):
        if self.speed_up:
            self.speed_up = False
        else:
            self.speed_up = True

    def run(self):
        self.gui = Gui()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                for btn in self.gui.all_buttons:
                    btn_cords = [btn.cord_x, btn.cord_y]

                    if event.type == pg.MOUSEBUTTONUP:
                        if event.button == 1:
                            if self.gui.in_button_area(btn_cords, event):
                                if btn.name == 'menu':
                                    self.gui.open_menu()
                                elif btn.name == 'pause':
                                    self.pause_continue()
                                    self.gui.change_pause_image()

                                elif btn.name == 'speed_up':
                                    self.speed_up_on_off()

                    if btn in self.gui.buildings_buttons or btn == self.gui.translucent_button:
                        if event.type == pg.MOUSEMOTION:
                            if event.buttons[0] == 1:
                                if self.gui.in_button_area(btn_cords, event):
                                    if not self.gui.translucent_button:
                                        self.gui.create_translucent_button(btn)
                                        btn = self.gui.translucent_button
                                        btn_cords = [btn.cord_x, btn.cord_y]

                                    if btn.movable:
                                        shift = event.rel
                                        btn.cord_x += shift[0]
                                        btn.cord_y += shift[1]

                        elif event.type == pg.MOUSEBUTTONUP:
                            if self.gui.translucent_button and \
                                    0 <= event.pos[0] <= width and 50 <= event.pos[1] <= height:

                                tower = self.gui.translucent_button.name[:-5]

                                tile_cords = list(event.pos)
                                tile_cords[1] -= 50
                                tile_cords = list(map(lambda num: num // 50, tile_cords))

                                self.board.add_tower(tower, tile_cords)

                                self.gui.translucent_button = None

                            elif self.gui.translucent_button:
                                self.gui.translucent_button = None

            if not self.pause:
                pass

            self.screen.fill(pg.Color(0, 0, 0))

            self.board.draw(self.board_surface)
            self.screen.blit(self.board_surface, (0, 50))

            self.gui.draw(self.gui_surface)
            self.screen.blit(self.gui_surface, (0, 0))

            if self.gui.translucent_button:
                self.gui.draw_translucent_button(self.screen)

            pg.display.flip()

    def terminate(self):
        pg.quit()
        sys.exit()