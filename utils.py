import pygame as pg


def load_image(filename, colorkey=None):
    image = pg.image.load(filename).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image