import pygame

from entities import PhysicsEntity
from pygame.locals import *

from utils import terminate, load_image

pygame.init()


class Game:
    def __init__(self, size):
        self.size = size

        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption("test")

        self.clock = pygame.time.Clock()

        self.assets = {
            "player": load_image("data/entities/player.png")
        }

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))

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
            self.surface.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key in (K_w, K_a, K_s, K_d):
                        self.user_input[event.key] = True
                if event.type == pygame.KEYUP:
                    if event.key in (K_w, K_a, K_s, K_d):
                        self.user_input[event.key] = False

            direction = self.user_input.get(K_d, False) - self.user_input.get(K_a, False)
            self.player.update((direction, 0))
            self.player.render(self.surface)

            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.run_start_screen()
        self.run_game()


game = Game((1400, 900))
game.run()