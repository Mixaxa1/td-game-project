import pygame as pg

from utils import load_image


class Gui:
    def __init__(self):
        self.system_buttons = [Button('menu', 'images/gear.png', [10, 10]),
                               Button('pause', 'images/continue.png', [60, 10]),
                               Button('speed_increase', 'images/speed_increase.png', [110, 10])]
        self.buildings_buttons = [Button('tower1', 'images/tower1.jpg', [210, 10]),
                                  Button('tower2', 'images/tower2.jpg', [260, 10])]
        self.translucent_button = None
        self.update_all_buttons()
        self.buttons_size = (30, 30)

    def draw(self, surface):
        surface.fill(pg.Color('gray'))

        self.update_all_buttons()

        for btn in self.all_buttons:
            image = load_image(btn.image, self.buttons_size, -1)
            surface.blit(image, (btn.cord_x, btn.cord_y))

    def draw_translucent_button(self, screen):
        image = load_image(self.translucent_button.image, self.buttons_size, -1)
        screen.blit(image, (self.translucent_button.cord_x, self.translucent_button.cord_y))

    def open_menu(self):
        print('На этом моменте должно было открытся меню')

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
    def __init__(self, name, image, cords, movable=False):
        self.name = name
        self.image = image
        self.cord_x = cords[0]
        self.cord_y = cords[1]
        self.movable = movable
