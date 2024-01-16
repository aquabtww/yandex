import sys

import pygame
from pygame.locals import *

pygame.init()


def load_image(path):
    return pygame.image.load(path).convert_alpha()


def terminate():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self, size):
        self.size = size

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("test")

        self.clock = pygame.time.Clock()

        self.user_input = {}

    def run_start_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            self.clock.tick(30)

    def run_game(self):
        while True:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key in (K_w, K_a, K_s, K_d):
                        self.user_input[event.key] = True
                if event.type == pygame.KEYUP:
                    if event.key in (K_w, K_a, K_s, K_d):
                        self.user_input[event.key] = False

            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.run_start_screen()
        self.run_game()


game = Game((600, 600))
game.run()