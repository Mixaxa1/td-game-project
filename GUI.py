import pygame as pg


class Gui:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, surface):
        surface.fill(pg.Color('red'))