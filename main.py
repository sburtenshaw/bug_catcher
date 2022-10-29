import sys
import pygame

from game import Game

from constants import WINDOW_SIZE, FRAMERATE

pygame.init()
pygame.font.init()


class Main:
    def __init__(self, window_size, framerate):
        self.window_size = window_size
        self.framerate = framerate

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Bug Catcher')

        self.game = Game(self.screen)

    def update(self, dt):
        self.game.update(dt)

    def draw(self):
        self.game.draw()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dt = self.clock.tick(self.framerate)

            self.update(dt)
            self.draw()

            pygame.display.flip()


main = Main(WINDOW_SIZE, FRAMERATE)
main.loop()
