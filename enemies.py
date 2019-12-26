import pygame as pg
from utils import load_image


class Enemy(pg.sprite.Sprite):
    image = load_image('images/enemy1.png', -1)

    def __init__(self, atk, hp, x1, y1,  *groups):
        super().__init__(*groups)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.attack_points, self.health_points = atk, hp
        self.rect.left, self.rect.top = x1, y1

    def move_to(self, x2, y2):
        self.rect.left = x2
        self.rect.top = y2

    def attack(self, target):
        target.hp -= self.attack_points
