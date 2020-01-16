import pygame as pg

from utils import load_image


class Gui:
    def __init__(self):
        self.system_buttons = [Button('menu', [10, 10], 'images/gear.png'),
                               Button('pause', [60, 10], 'images/continue.png'),
                               Button('speed_up', [110, 10], 'images/speed_up.png')]
        self.buildings_buttons = [Button('tower1', [210, 10], 'images/tower1.jpg'),
                                  Button('tower2', [260, 10], 'images/tower2.jpg')]
        self.manu_buttons = ['Продолжить', 'Выход']
        self.translucent_button = None
        self.update_all_buttons()
        self.buttons_size = (30, 30)

        self.hp_font = pg.font.SysFont(None, 30)

    def draw_gui(self, surface, hp):
        surface.fill(pg.Color('gray'))

        self.update_all_buttons()

        for btn in self.all_buttons:
            image = load_image(btn.image, self.buttons_size, -1)
            surface.blit(image, (btn.cord_x, btn.cord_y))

        self.draw_hp(surface, hp)

    def draw_hp(self, surface, hp):
        heart_image = load_image('images/heart.png', (20, 20), -1)
        surface.blit(heart_image, (457, 10))

        hp_text = self.hp_font.render(str(hp), 0, pg.color.Color('black'))
        surface.blit(hp_text, (450, 30))

    def draw_translucent_button(self, screen):
        image = load_image(self.translucent_button.image, self.buttons_size, -1)
        screen.blit(image, (self.translucent_button.cord_x, self.translucent_button.cord_y))

    def draw_menu(self, menu):
        menu.fill((31, 9, 6))
        menu.set_alpha(150)

        button = pg.Surface((100, 50))
        button.fill((255, 9, 6))
        menu.blit(button, (100, 100))

    def change_pause_image(self):
        if self.system_buttons[1].image == 'images/continue.png':
            self.system_buttons[1].image = 'images/pause.png'
        else:
            self.system_buttons[1].image = 'images/continue.png'

    def create_translucent_button(self, btn):
        self.translucent_button = Button(btn.name + ' copy', btn.image, (btn.cord_x, btn.cord_y), True)

    def in_button_area(self, cords, event):
        return cords[0] <= event.pos[0] <= cords[0] + self.buttons_size[0] and \
               cords[1] <= event.pos[1] <= cords[1] + self.buttons_size[1]

    def update_all_buttons(self):
        self.all_buttons = self.system_buttons + self.buildings_buttons

        if self.translucent_button:
            self.all_buttons.append(self.translucent_button)


class Button:
    def __init__(self, name, cords, image=None, movable=False):
        self.name = name
        self.image = image
        self.cord_x = cords[0]
        self.cord_y = cords[1]
        self.movable = movable
