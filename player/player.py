import pygame
import uuid

from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from support import timeout, get_rects_collided, rotate_pivot, convert_vector_to_angle
from .bullet import Bullet

PLAYER_WIDTH, PLAYER_HEIGHT = 96, 96
PLAYER_SPEED = 5
PLAYER_FIRE_DELAY = 500


class Player:
    def __init__(self, screen, bugs):
        self.screen = screen
        self.bugs = bugs

        self.player_image = self.get_player_image()
        self.player_rect = self.get_player_rect()

        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 1)
        self.angle = 0

        self.score = 0
        self.lost = 0

        self.bullets = {}
        self.firing = False

    def get_player_image(self):
        return pygame.transform.scale(
            pygame.image.load('images/spider.png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

    def get_player_rect(self):
        return self.player_image.get_rect(
            centerx=WINDOW_WIDTH * 0.5,
            centery=WINDOW_HEIGHT * 0.5,
        )

    def set_firing(self, firing):
        self.firing = firing

    def get_bullet_direction(self):
        # the bullet shoots in the opposite direction to the player direction
        y_direction = self.direction.y * -1
        if self.direction.y == 0 and self.direction.x == 0:
            y_direction = -1
        return pygame.math.Vector2(
            self.direction.x * -1,
            y_direction
        )

    def fire_bullet(self):
        # the user cannot fire again while firing is true
        self.set_firing(True)

        # generate a unique identifier for the bullet
        bullet_id = uuid.uuid4()
        self.bullets[bullet_id] = Bullet(
            self.screen,
            pygame.math.Vector2(self.player_rect.center),
            self.get_bullet_direction(),
            bullet_id,
            self.bugs
        )

        # set firing to false after X time
        timeout(self.set_firing, PLAYER_FIRE_DELAY, False)

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()

        # reset y direction when x direction key pressed
        if (
            keys_pressed[pygame.K_LEFT] or
            keys_pressed[pygame.K_RIGHT]
        ):
            self.direction.y = 0

        # reset x direction when y direction key pressed
        if (
            keys_pressed[pygame.K_UP] or
            keys_pressed[pygame.K_DOWN]
        ):
            self.direction.x = 0

        # left and right velocity
        if keys_pressed[pygame.K_LEFT] and self.player_rect.x > 0:
            self.velocity.x = -1
            self.direction.x = 1
        elif keys_pressed[pygame.K_RIGHT] and self.player_rect.x + self.player_rect.width < WINDOW_WIDTH:
            self.velocity.x = 1
            self.direction.x = -1
        else:
            self.velocity.x = 0

        # up and down velocity
        if keys_pressed[pygame.K_UP] and self.player_rect.y > 0:
            self.velocity.y = -1
            self.direction.y = 1
        elif keys_pressed[pygame.K_DOWN] and self.player_rect.y + self.player_rect.height < WINDOW_HEIGHT:
            self.velocity.y = 1
            self.direction.y = -1
        else:
            self.velocity.y = 0

        # fire bullet
        if keys_pressed[pygame.K_SPACE] and not self.firing:
            self.fire_bullet()

    def update_bullets(self, dt):
        # list of bullet ids to delete
        bullets_to_delete = []

        # add bullets set to delete to array or update bullets
        for bullet in self.bullets.values():
            if bullet.delete:
                bullets_to_delete.append(bullet.bullet_id)
            else:
                bullet.update(dt)

        # delete bullets that are in array
        for bullet_id in bullets_to_delete:
            del self.bullets[bullet_id]

    def check_bug_collision(self):
        for bug in self.bugs.values():
            if get_rects_collided(self.player_rect, bug.bug_rect) and bug.stuck:
                bug.delete = True
                self.score += 1

    def update(self, dt):
        self.handle_input()

        # normalise velocities
        if self.velocity.x or self.velocity.y:
            self.velocity = self.velocity.normalize()

        # update player position
        self.player_rect = self.player_rect.move(
            PLAYER_SPEED * self.velocity.x * dt,
            PLAYER_SPEED * self.velocity.y * dt
        )

        self.check_bug_collision()

        self.update_bullets(dt)

    def draw(self):
        # draw bullets
        for bullet in self.bullets.values():
            bullet.draw()

        # get rotated player image
        rotated_player_image, rotated_player_image_rect = rotate_pivot(
            self.player_image,
            convert_vector_to_angle(self.direction),
            self.player_rect.center
        )

        # draw player
        self.screen.blit(
            rotated_player_image,
            rotated_player_image_rect
        )
