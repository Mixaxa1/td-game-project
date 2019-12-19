import sys
import pygame

from TDGame import Game

pygame.init()

width = 1000
height = 1000


def terminate():
    pygame.quit()
    sys.exit()


game = Game(width, height)
game.start()

terminate()