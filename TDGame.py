import os
import sys
import time

import pygame as pg

from Board import Board
from GUI import Gui
from utils import load_image
from buildings import buildings_factory

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
        self.pause_start = 0

        self.hp = 50
        self.money = 20
        self.difficulty = 1

        self.tracers = []

        self.board_surface = pg.Surface((500, 500))
        self.gui_surface = pg.Surface((500, 50))
        self.menu_surface = pg.Surface((500, 550))

        self.start_screen()

    def start_screen(self):
        intro_text = ["                          TOWER DEFENSE", "",
                      "       Нажмите любую клавишу для начала игры"]

        fon = load_image('images/background.jpg', (500, 550))
        screen.blit(fon, (0, 0))
        font = pg.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pg.Color('BLACK'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.terminate()
                elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    return
            pg.display.flip()

            self.load_level()

    def load_level(self):
        field = [['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 's', 's', 's', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 'g', 'g', 's', 'g', 'g', 'g', 'g', 'g'],
                 ['g', 's', 's', 'g', 's', 's', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 's', 'g', 'g', 's', 'g', 'g', 'g', 'g'],
                 ['g', 'g', 's', 'g', 'g', 's', 'g', 's', 's', 'sb'],
                 ['s', 's', 's', 'g', 'g', 's', 'g', 's', 'g', 'g'],
                 ['g', 'g', 'g', 'g', 'g', 's', 's', 's', 'g', 'g'],
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
            if self.pause_start != 0:
                pause_end = time.clock()
                for tower in self.board.towers:
                    tower.time_adjustment = pause_end - self.pause_start
        else:
            self.pause = True
            self.pause_start = time.clock()

        self.gui.change_pause_image()

    def speed_up_on_off(self):
        if self.speed_up == 1:
            self.speed_up = 2
        else:
            self.speed_up = 1

        self.gui.change_speed_increase_image()

    def on_finish(self, enemy):
        if self.board.base.pos_x + 50 >= enemy.pos_x + 15 >= self.board.base.pos_x and \
                self.board.base.pos_y + 50 >= enemy.pos_y + 15 >= self.board.base.pos_y:
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

                                col, row = tile_cords
                                tower = buildings_factory(tower, col, row, (), 50, 50)
                                if self.board.field[row][col].for_towers and not self.board.field[row][col].built_up \
                                        and self.money >= tower.cost:
                                    self.money -= tower.cost
                                    self.board.buildings_group.add(tower)
                                    self.board.towers_group.add(tower)
                                    self.board.add_tower(tower, tile_cords)

                                self.gui.translucent_button = None

                            elif self.gui.translucent_button:
                                self.gui.translucent_button = None

            if not self.pause:
                for tower in self.board.towers:
                    for enemy in self.board.enemies:
                        if tower.determine_distance(enemy) <= tower.attack_range:
                            if time.clock() - tower.last_shot_time - tower.time_adjustment >= tower.reload_time:
                                tower.last_shot_time = time.clock()
                                tower.shot(enemy)
                                tower.last_shot_time = time.clock()
                                tower.time_adjustment = 0

                                if enemy.hp <= 0:
                                    self.money += enemy.reward
                                    self.board.kill_enemy(enemy)

                                self.tracers.append([(tower.pos_x + 25, tower.pos_y + 75),
                                                     (enemy.pos_x + 10, enemy.pos_y + 60), 5])
                                break

                for enemy in self.board.enemies:
                    if not self.on_finish(enemy):
                        enemy.step(self.speed_up)

                    else:
                        self.hp -= enemy.dmg
                        self.board.kill_enemy(enemy)

                if not self.board.enemies:
                    self.board.start_new_wave(self.difficulty)
                    self.difficulty += 1

            self.screen.fill(pg.Color(0, 0, 0))

            self.board.draw(self.board_surface)
            self.screen.blit(self.board_surface, (0, 50))

            self.gui.draw_gui(self.gui_surface, self.hp, self.money)
            self.screen.blit(self.gui_surface, (0, 0))

            if self.menu_open:
                self.gui.draw_menu(self.menu_surface, screen)

            if self.gui.translucent_button:
                self.gui.draw_translucent_button(self.screen)

            to_delete = []
            for i in range(len(self.tracers)):
                if self.tracers[i][2] > 0:
                    pg.draw.line(screen, (0, 0, 0), self.tracers[i][0], self.tracers[i][1])
                    self.tracers[i][2] -= 1
                else:
                    to_delete.append(self.tracers[i])
            self.tracers = [tracer for tracer in self.tracers if tracer not in to_delete]

            if self.hp <= 0:
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
        while 1 == 1:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        os.system('restart.py')
                        self.terminate()
                    elif event.key == pg.K_ESCAPE:
                        self.terminate()

    def terminate(self):
        pg.quit()
        sys.exit()
