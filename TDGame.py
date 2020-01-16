import os
import sys

import pygame as pg

from Board import Board
from GUI import Gui
from utils import load_image
import buildings

pg.init()
size = width, height = 500, 550
screen = pg.display.set_mode(size)


class GameOver(pg.sprite.Sprite):
    image_to_draw = load_image('images/gameover.png', (500, 550))

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.image_to_draw
        self.rect = self.image_to_draw.get_rect()
        self.rect.x = -500
        self.rect.y = 0


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = width
        self.screen_height = height

        self.screen = pg.display.set_mode((screen_width, screen_height))

        self.running = False
        self.pause = True
        self.menu_open = False
        self.speed_up = 1

        self.hp = 50
        self.difficulty = 1

        self.board_surface = pg.Surface((500, 500))
        self.gui_surface = pg.Surface((500, 50))
        self.menu_surface = pg.Surface((500, 550))

        self.load_level()

    def load_level(self):
        field = [['g', 'g', 'g', 'g', 't1', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'sb', 's', 's', 'sb', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 'g', 'g', 's', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'sb', 'sb', 'g', 'sb', 'sb', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 's', 'g', 'g', 's', 'g', 't1', 'g', 'g'],
                 ['g', 't1', 's', 'g', 'g', 's', 'g', 'sb', 's', 'sb'],
                 ['s', 's', 'sb', 'g', 'g', 's', 'g', 's', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'sb', 's', 'sb', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]

        width, height = len(field), len(field[0])
        self.board = Board(width, height, field)

    def start(self):
        self.running = True
        self.run()

    def open_menu(self):
        self.menu_open = True
        self.gui.draw_menu(self.menu_surface, screen)

    def pause_continue(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True

        self.gui.change_pause_image()

    def speed_up_on_off(self):
        if self.speed_up == 1:
            self.speed_up = 2
        else:
            self.speed_up = 1

    def on_finish(self, enemy):
        # if self.board.base.pos_x + 50 >= enemy.pos_x + 15 >= self.board.base.pos_x and \
        #         self.board.base.pos_y + 50 >= enemy.pos_x + 15 >= self.board.base.pos_y:
        # закоментировано до добавления базы
        if 500 >= enemy.pos_x + 15 >= 450 and 300 >= enemy.pos_y + 15 >= 250:
            return True
        return False

    def run(self):
        self.gui = Gui()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                for btn in self.gui.buttons + self.gui.menu_buttons:
                    btn_cords = [btn.cord_x, btn.cord_y]

                    if event.type == pg.MOUSEBUTTONUP:
                        if event.button == 1:
                            if self.gui.in_button_area(btn, event):
                                if btn.name == 'menu' and not self.menu_open:
                                    self.open_menu()
                                elif btn.name == 'pause' and not self.menu_open:
                                    self.pause_continue()
                                elif btn.name == 'speed_up' and not self.menu_open:
                                    self.speed_up_on_off()
                                elif btn.name == 'Продолжить':
                                    self.menu_open = False
                                elif btn.name == 'Выход':
                                    self.terminate()

                    if btn in self.gui.buildings_buttons or btn == self.gui.translucent_button:
                        if event.type == pg.MOUSEMOTION:
                            if event.buttons[0] == 1:
                                if self.gui.in_button_area(btn, event):
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
                for enemy in self.board.enemies:
                    if not self.on_finish(enemy):
                        enemy.step(self.speed_up)

                    else:
                        self.hp -= enemy.dmg
                        self.board.enemies.remove(enemy)
                        self.board.kill_enemy(enemy)

                if not self.board.enemies:
                    self.board.start_new_wave(self.difficulty)
                    self.difficulty += 1

            self.screen.fill(pg.Color(0, 0, 0))

            self.board.draw(self.board_surface)
            self.screen.blit(self.board_surface, (0, 50))

            self.gui.draw_gui(self.gui_surface, self.hp)
            self.screen.blit(self.gui_surface, (0, 0))

            if self.menu_open:
                self.gui.draw_menu(self.menu_surface, screen)

            if self.gui.translucent_button:
                self.gui.draw_translucent_button(self.screen)

            if self.hp == 0:
                self.game_over()

            pg.display.flip()

    def game_over(self):
        clock = pg.time.Clock()
        tmp_group = pg.sprite.Group()
        gameover = GameOver(tmp_group)
        while gameover.rect.x != 0:
            gameover.rect.x += 2
            tmp_group.draw(self.screen)
            pg.display.flip()
            clock.tick(50)
        print('The game is over, would you like to restart?')
        answer = input().lower().strip()
        if answer == 'yes':
            os.system('python restart.py')
            self.terminate()
        else:
            self.terminate()

    def terminate(self):
        pg.quit()
        sys.exit()
