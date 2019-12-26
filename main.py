import sys
import pygame

from TDGame import Game

pygame.init()

width = 500
height = 550


def terminate():
    pygame.quit()
    sys.exit()


game = Game(width, height)
game.start()

terminate()