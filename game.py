from title import Title
from level import Level


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.high_score = 0

        self.view = None

        self.load_title()

    def load_title(self, score=None):
        if score and score > self.high_score:
            self.high_score = score

        self.view = Title(self.screen, self.load_level, self.high_score)

    def load_level(self):
        self.view = Level(self.screen, self.load_title, self.high_score)

    def update(self, dt):
        self.view.update(dt)

    def draw(self):
        self.view.draw()
