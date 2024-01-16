import sys

import pygame


def load_image(path):
    return pygame.image.load(path).convert_alpha()


def terminate():
    pygame.quit()
    sys.exit()