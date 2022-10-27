import pygame
import uuid

from player import Player
from bug import Bug

MAX_BUGS = 10
MAX_LOST = 10
BUG_SPAWN_TIME = 15000


class Level:
    def __init__(self, screen, load_title, high_score):
        self.screen = screen
        self.load_title = load_title
        self.high_score = high_score

        self.start_time = pygame.time.get_ticks()

        self.background_image = pygame.image.load('images/background_web.png')
        self.background_rect = self.background_image.get_rect(x=0, y=0)

        self.bugs = {}
        self.player = Player(self.screen, self.bugs)

        self.high_score_text = pygame.font.SysFont('Comic Sans MS', 32)
        self.score_text = pygame.font.SysFont('Comic Sans MS', 32)
        self.lost_text = pygame.font.SysFont('Comic Sans MS', 32)

    def update_bugs(self, dt):
        # list of bug ids to delete
        bugs_to_delete = []

        # add bugs set to delete to array or update bugs
        for bug in self.bugs.values():
            if bug.delete:
                bugs_to_delete.append(bug.bug_id)
            else:
                bug.update(dt)

        # delete bugs that are in array
        for bug_id in bugs_to_delete:
            del self.bugs[bug_id]

    def create_bug(self):
        # generate a unique identifier for the bug
        bug_id = uuid.uuid4()
        self.bugs[bug_id] = Bug(self.screen, self.player, bug_id)

    def create_bugs(self):
        # get the current time elapsed in the game
        time = pygame.time.get_ticks()

        # create more bugs as more time goes on
        if len([bug for bug in self.bugs.values() if not bug.stuck]) < min((time - self.start_time) / BUG_SPAWN_TIME, MAX_BUGS):
            self.create_bug()

    def update(self, dt):
        # game ends when the player loses X bugs
        if self.player.lost >= MAX_LOST:
            self.load_title(self.player.score)

        keys_pressed = pygame.key.get_pressed()

        # end game if escape key pressed
        if keys_pressed[pygame.K_ESCAPE]:
            self.load_title()

        self.player.update(dt)

        self.update_bugs(dt)

        self.create_bugs()

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)

        for bug in self.bugs.values():
            bug.draw()

        self.player.draw()

        # render high score text
        self.screen.blit(self.high_score_text.render(
            f'High Score: {self.high_score}',
            False,
            (0, 0, 0)
        ), (32, 32))

        # render score text
        self.screen.blit(self.score_text.render(
            f'Score: {self.player.score}',
            False,
            (0, 0, 0)
        ), (32, 72))

        # render lost text
        self.screen.blit(self.lost_text.render(
            f'Lost: {self.player.lost}',
            False,
            (0, 0, 0)
        ), (32, 112))
