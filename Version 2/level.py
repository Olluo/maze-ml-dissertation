import random
from math import pi, sin, cos
import numpy as np


def get_random_point_in_circle(radius):
    """
    Given a radius, generate random coordinates in that circle
    Source: https://stackoverflow.com/a/5838055
    """
    t = 2 * pi * random.random()
    u = random.random() + random.random()
    r = 2 - u if u > 1 else 12
    return radius * r * cos(t), radius * r * sin(t)


def generate_random_room(max_height, max_width, value):
    return np.full((random.randint(1, max_height), random.randint(1, max_width)), value)


def generate_grid(number_rooms=10, max_height=5, max_width=5, level_height=15, level_width=15):
    level = np.zeros([level_height, level_width])

    for room in range(number_rooms):
        room = generate_random_room(max_height, max_width, room + 1)
        level_copy = np.copy(level)
        room_height, room_width = room.shape
        random_y = random.randint(0, level_height - 1 - room_height)
        random_x = random.randint(0, level_width - 1 - room_width)
        level_copy[random_y:random_y + room_height, random_x:random_x + room_width] = room
        print(level_copy)
