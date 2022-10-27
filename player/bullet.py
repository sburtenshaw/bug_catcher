import pygame

from support import (
    get_rect_visible,
    get_rects_collided,
    rotate_pivot,
    convert_vector_to_angle
)

BULLET_WIDTH, BULLET_HEIGHT = 24, 24
BULLET_SPEED = 10


class Bullet:
    def __init__(self, screen, initial_position, direction, bullet_id, bugs):
        self.screen = screen
        self.initial_position = initial_position
        self.direction = direction
        self.bullet_id = bullet_id
        self.bugs = bugs

        self.bullet_image = self.get_bullet_image()
        self.bullet_rect = self.get_bullet_rect()

        self.delete = False

    def get_bullet_image(self):
        return pygame.transform.scale(
            pygame.image.load('images/web_shot.png'),
            (BULLET_HEIGHT, BULLET_HEIGHT)
        )

    def get_bullet_rect(self):
        return self.bullet_image.get_rect(
            centerx=self.initial_position.x,
            centery=self.initial_position.y
        )

    def check_bug_collision(self):
        for bug in self.bugs.values():
            if get_rects_collided(self.bullet_rect, bug.bug_rect) and not bug.stuck:
                bug.set_stuck(True)
                self.delete = True

    def update(self, dt):
        # update bullet position
        self.bullet_rect = self.bullet_rect.move(
            BULLET_SPEED * self.direction.x * -1 * dt,
            BULLET_SPEED * self.direction.y * -1 * dt
        )

        # destroy the bullet if it becomes invisible
        if not get_rect_visible(self.bullet_rect):
            self.delete = True

        # check if the bullet has collided with a bug
        self.check_bug_collision()

    def draw(self):
        # get rotated bullet image
        rotated_bullet_image, rotated_bullet_image_rect = rotate_pivot(
            self.bullet_image,
            convert_vector_to_angle(self.direction),
            self.bullet_rect.center
        )

        # draw bullet
        self.screen.blit(
            rotated_bullet_image,
            rotated_bullet_image_rect
        )
