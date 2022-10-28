import pygame
import uuid

from bug import Bug

from support import timeout, update_or_delete

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

BUG_CREATE_DELAY = 2000


class Title:
    def __init__(self, screen, load_level, high_score):
        self.screen = screen
        self.load_level = load_level
        self.high_score = high_score

        self.background_image = pygame.image.load('images/background_web.png')
        self.background_rect = self.background_image.get_rect(x=0, y=0)

        self.bugs = {}
        self.creating_bug = False

        self.title_text = pygame.font.SysFont('Comic Sans MS', 64)
        self.start_text = pygame.font.SysFont('Comic Sans MS', 48)
        self.high_score_text = pygame.font.SysFont('Comic Sans MS', 32)

    def set_creating_bug(self, creating):
        self.creating_bug = creating

    def create_bugs(self):
        if len(self.bugs.keys()) < 10 and not self.creating_bug:
            self.set_creating_bug(True)
            id = uuid.uuid4()
            self.bugs[id] = Bug(self.screen, None, id)
            timeout(self.set_creating_bug, BUG_CREATE_DELAY, False)

    def update(self, dt):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RETURN]:
            self.load_level()

        update_or_delete(self.bugs,  dt)

        self.create_bugs()

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)

        for bug in self.bugs.values():
            bug.draw()

        # render title text
        title_text_surface = self.title_text.render(
            'Bug Catcher',
            False,
            (0, 0, 0)
        )
        self.screen.blit(title_text_surface, (
            WINDOW_WIDTH * 0.5 - title_text_surface.get_width() * 0.5,
            WINDOW_HEIGHT * 0.5 - title_text_surface.get_height() * 2,
        ))

        # render start text
        start_text_surface = self.start_text.render(
            'Press Enter To Start',
            False,
            (0, 0, 0)
        )
        self.screen.blit(start_text_surface, (
            WINDOW_WIDTH * 0.5 - start_text_surface.get_width() * 0.5,
            WINDOW_HEIGHT * 0.5 - start_text_surface.get_height() * 0.5,
        ))

        # render high score text
        high_score_text_surface = self.high_score_text.render(
            f'High Score: {self.high_score}',
            False,
            (0, 0, 0)
        )
        self.screen.blit(high_score_text_surface, (
            WINDOW_WIDTH * 0.5 - high_score_text_surface.get_width() * 0.5,
            WINDOW_HEIGHT * 0.5 + high_score_text_surface.get_height() * 2,
        ))
