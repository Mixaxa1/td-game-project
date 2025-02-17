import pygame as pg

from utils import load_image


class Gui:
    def __init__(self):
        self.system_buttons = [Button('menu', [10, 10], (30, 30), 'images/gear.png'),
                               Button('pause', [60, 10], (30, 30), 'images/continue.png'),
                               Button('speed_up', [110, 10], (30, 30), 'images/speed_up.png')]
        self.buildings_buttons = [Button('ArcherTower', [210, 3], (30, 30), 'images/ArcherTower.jpg'),
                                  Button('BallisticTower', [260, 3], (30, 30), 'images/BallisticTower.jpg'),
                                  Button('MagicTower', [310, 3], (30, 30), 'images/MagicTower.jpg')]
        self.menu_buttons = [Button('Продолжить', [175, 100], (150, 50)), Button('Выход', [175, 200], (150, 50))]
        self.prices = [(15, (210, 32)), (20, (260, 32)), (25, (310, 32))]
        self.translucent_button = None
        self.update_buttons()

        self.font = pg.font.SysFont(None, 30)
        self.prices_font = pg.font.SysFont(None, 30)

    def draw_gui(self, surface, hp, money):
        surface.fill(pg.Color('gray'))

        self.update_buttons()

        for btn in self.buttons:
            image = load_image(btn.image, btn.size, -1)
            surface.blit(image, (btn.cord_x, btn.cord_y))

        self.draw_hp(surface, hp)
        self.draw_money(surface, money)
        self.draw_prices(surface)

    def draw_hp(self, surface, hp):
        heart_image = load_image('images/heart.png', (20, 20), -1)
        surface.blit(heart_image, (457, 10))

        if hp < 0:
            hp = 0

        hp_text = self.font.render(str(hp), 0, pg.color.Color('black'))
        surface.blit(hp_text, (450, 30))

    def draw_money(self, surface, money):
        money_image = load_image('images/money.png', (20, 20), -1)
        surface.blit(money_image, (400, 10))

        money_text = self.font.render(str(money), 0, pg.color.Color('black'))
        surface.blit(money_text, (400, 30))

    def draw_prices(self, surface):
        for price in self.prices:
            price_text = self.font.render(str(price[0]), 0, pg.color.Color('black'))
            surface.blit(price_text, (price[1]))

    def draw_translucent_button(self, screen):
        image = load_image(self.translucent_button.image, (30, 30), -1)
        screen.blit(image, (self.translucent_button.cord_x, self.translucent_button.cord_y))

    def draw_menu(self, menu, screen):
        menu.fill((31, 9, 6))
        menu.set_alpha(150)
        screen.blit(menu, (0, 0))

        for btn in self.menu_buttons:
            button = pg.Surface(btn.size)
            button.fill((255, 9, 6))

            button_text = self.font.render(btn.name, 0, pg.color.Color('black'))
            button.blit(button_text, (5, 15))

            screen.blit(button, (btn.cord_x, btn.cord_y))

    def change_pause_image(self):
        if self.system_buttons[1].image == 'images/continue.png':
            self.system_buttons[1].image = 'images/pause.png'
        else:
            self.system_buttons[1].image = 'images/continue.png'

    def change_speed_increase_image(self):
        if self.system_buttons[2].image == 'images/speed_up.png':
            self.system_buttons[2].image = 'images/speed_increase.png'
        else:
            self.system_buttons[2].image = 'images/speed_up.png'

    def create_translucent_button(self, btn):
        self.translucent_button = Button(btn.name + ' copy', (btn.cord_x, btn.cord_y), (30, 30), btn.image, True)

    def in_button_area(self, btn, event):
        return btn.cord_x <= event.pos[0] <= btn.cord_x + btn.size[0] and \
               btn.cord_y <= event.pos[1] <= btn.cord_y + btn.size[1]

    def update_buttons(self):
        self.buttons = self.system_buttons + self.buildings_buttons

        if self.translucent_button:
            self.buttons.append(self.translucent_button)


class Button:
    def __init__(self, name, cords, size, image=None, movable=False):
        self.name = name
        self.image = image
        self.cord_x = cords[0]
        self.cord_y = cords[1]
        self.size = size
        self.movable = movable
