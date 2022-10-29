import pygame
from random import randrange

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from support import timeout, get_rect_visible, rotate_pivot

BUG_WIDTH, BUG_HEIGHT = 32, 32
BUG_SPEED = 0.2
BUG_MAX_STUCK = 5000


class Bug:
    def __init__(self, screen, player,  id):
        self.screen = screen
        self.player = player
        self.id = id

        self.first_visible = False
        self.stuck = False
        self.delete = False
        self.velocity = pygame.math.Vector2(0, 0)

        self.bug_image = self.get_bug_image()
        self.bug_rect = self.get_bug_rect()

        self.set_initial_state()

    def get_bug_image(self):
        return pygame.transform.scale(
            pygame.image.load('images/fly.png'),
            (BUG_WIDTH, BUG_HEIGHT)
        )

    def get_bug_rect(self):
        return self.bug_image.get_rect(x=0, y=0)

    def get_initial_state(self):
        position = ['left', 'up', 'right', 'down'][randrange(4)]
        if position == 'left':
            return (-32, randrange(64, WINDOW_HEIGHT - 64), 1, 0, 270)
        elif position == 'up':
            return (randrange(64, WINDOW_WIDTH - 64), -32, 0, 1, 180)
        elif position == 'right':
            return (WINDOW_WIDTH, randrange(64, WINDOW_HEIGHT - 64), -1, 0, 90)
        else:
            return (randrange(64, WINDOW_WIDTH - 64), WINDOW_HEIGHT, 0, -1, 0)

    def set_initial_state(self):
        x_pos, y_pos, x_vel, y_vel, angle = self.get_initial_state()
        self.velocity.x = x_vel
        self.velocity.y = y_vel
        rotated_bug_image, rotated_bug_image_rect = rotate_pivot(
            self.bug_image,
            angle,
            (x_pos, y_pos)
        )
        self.bug_image = rotated_bug_image
        self.bug_rect = rotated_bug_image_rect

    def set_stuck(self, stuck):
        self.stuck = stuck

        # unstick itself after X time
        if self.stuck:
            timeout(self.set_stuck, BUG_MAX_STUCK, False)

    def update(self, dt):
        # move the bug if it's not stuck
        if not self.stuck:
            self.bug_rect = self.bug_rect.move(
                BUG_SPEED * self.velocity.x * dt,
                BUG_SPEED * self.velocity.y * dt
            )

        # delete the bug if it has become visible and then become invisible
        if get_rect_visible(self.bug_rect) and not self.first_visible:
            self.first_visible = True
        elif not get_rect_visible(self.bug_rect) and self.first_visible:
            self.delete = True
            if self.player:
                self.player.lost += 1

    def draw(self):
        self.screen.blit(self.bug_image, self.bug_rect)
