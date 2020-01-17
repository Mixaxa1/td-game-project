import pygame as pg


def load_image(filename, size, colorkey=None):
    image = pg.image.load(filename).convert()
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image