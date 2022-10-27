import sys
import pygame
import time

from title import Title
from level import Level

from constants import WINDOW_SIZE, FRAMERATE

pygame.init()
pygame.font.init()


class Game:
    def __init__(self, window_size, framerate):
        self.window_size = window_size
        self.framerate = framerate

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.last_time = time.time()

        self.high_score = 0

        self.view = None

        pygame.display.set_caption('Bug Catcher')

        self.load_title()

    def load_level(self):
        self.view = Level(self.screen, self.load_title, self.high_score)

    def load_title(self, score=None):
        if score and score > self.high_score:
            self.high_score = score

        self.view = Title(self.screen, self.load_level, self.high_score)

    def update(self, dt):
        self.view.update(dt)

    def draw(self):
        self.view.draw()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dt = (time.time() - self.last_time) * self.framerate
            self.last_time = time.time()

            self.update(dt)
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.framerate)


game = Game(WINDOW_SIZE, FRAMERATE)
game.loop()
