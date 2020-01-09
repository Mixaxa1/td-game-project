import pygame as pg
from utils import load_image


class Enemy(pg.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, path, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.path = path

        self.on_finish = False

        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.find_target_location()

    def find_target_location(self):
        if not self.path:
            self.on_finish = True
        else:
            self.x_count = (self.path[0].pos_x + 10 - self.pos_x) / self.speed
            self.y_count = (self.path[0].pos_y + 10 - self.pos_y) / self.speed

            self.path.pop(0)

    def step(self):
        if self.x_count == 0 and self.y_count == 0:
            self.find_target_location()

        if self.x_count > 0:
            self.pos_x += self.speed
            self.x_count -= 1
        elif self.x_count < 0:
            self.pos_x -= self.speed
            self.x_count += 1

        if self.y_count > 0:
            self.pos_y += self.speed
            self.y_count -= 1
        elif self.y_count < 0:
            self.pos_y -= self.speed
            self.y_count += 1

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y


class EnemyTest(Enemy):
    def __init__(self, x1, y1, path, groups):
        self.image = load_image('images/enemy1.png', (30, 30), -1)
        self.hp = 20
        self.speed = 1
        super().__init__(self.image, x1, y1, path, groups)
