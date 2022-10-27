import pygame
from threading import Timer

from constants import WINDOW_WIDTH, WINDOW_HEIGHT


def timeout(function, time, *args, **kwargs):
    t = Timer(time / 1000, function, args=args, kwargs=kwargs)
    t.start()
    return t


def get_rect_visible(rect):
    return (
        rect.x + rect.width > 0 and
        rect.x < WINDOW_WIDTH and
        rect.y + rect.height > 0 and
        rect.y < WINDOW_HEIGHT
    )


def get_rects_collided(rect_one, rect_two):
    return (
        rect_one.x < rect_two.x + rect_two.width and
        rect_one.x + rect_one.width > rect_two.x and
        rect_one.y < rect_two.y + rect_two.height and
        rect_one.height + rect_one.y > rect_two.y
    )


def rotate_pivot(image, angle, pivot):
    image_copy = pygame.transform.rotate(image, angle)
    image_rect = image_copy.get_rect()
    image_rect.center = pivot
    return image_copy, image_rect


def convert_vector_to_angle(vector):
    if vector.x == 0 and vector.y == 0:
        return 0
    elif vector.x == 0 and vector.y == 1:
        return 0
    elif vector.x == 1 and vector.y == 1:
        return 45
    elif vector.x == 1 and vector.y == 0:
        return 90
    elif vector.x == 1 and vector.y == -1:
        return 135
    elif vector.x == 0 and vector.y == -1:
        return 180
    elif vector.x == -1 and vector.y == -1:
        return 225
    elif vector.x == -1 and vector.y == 0:
        return 270
    elif vector.x == -1 and vector.y == 1:
        return 315
    else:
        return 0
