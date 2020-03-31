import random
from collections import namedtuple
from enum import IntEnum, auto

import numpy as np

# All the possible configurations of the doors of a room [North, South, East, West]
DOOR_CONFIGS = [
    [True, False, False, False],
    [False, True, False, False],
    [False, False, True, False],
    [False, False, False, True],

    [True, True, False, False],
    [True, False, False, True],
    [False, False, True, True],
    [True, False, True, False],
    [False, True, False, True],
    [False, True, True, False],

    [True, True, True, False],
    [True, True, False, True],
    [True, False, True, True],
    [False, True, True, True],
]
# The starting room has all doors open
START_ROOM = [True, True, True, True]

# Rooms that can be place to the north of the current room
NORTH_ROOMS = [config for config in DOOR_CONFIGS if config[1] is True]
# Rooms that can be place to the south of the current room
SOUTH_ROOMS = [config for config in DOOR_CONFIGS if config[0] is True]
# Rooms that can be place to the east of the current room
EAST_ROOMS = [config for config in DOOR_CONFIGS if config[3] is True]
# Rooms that can be place to the west of the current room
WEST_ROOMS = [config for config in DOOR_CONFIGS if config[2] is True]

# The caps are to be used when the level-gen gets to the edge of the map
NORTH_CAP = DOOR_CONFIGS[1]
SOUTH_CAP = DOOR_CONFIGS[0]
EAST_CAP = DOOR_CONFIGS[3]
WEST_CAP = DOOR_CONFIGS[2]

PersonalityTrait = namedtuple('PersonalityTrait', 'type, strength')


class PlayerType(IntEnum):
    ACHIEVER = auto()  # Collect as many points as possible
    ESCAPIST = auto()  # Escape the dungeon as soon as possible
    EXPLORER = auto()  # Explore as many rooms as possible
    KILLER = auto()  # Kill as many enemies as possible


class EntityType(IntEnum):
    ENEMY = auto()
    ROOM = auto()
    DOOR = auto()
    TREASURE = auto()
    # KEY = auto()
    PLAYER = auto()


class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    def opposite(self):
        if self.value == Direction.NORTH:
            return Direction.SOUTH
        elif self.value == Direction.SOUTH:
            return Direction.NORTH
        elif self.value == Direction.EAST:
            return Direction.WEST
        elif self.value == Direction.WEST:
            return Direction.EAST

    def rooms(self):
        if self.value == Direction.NORTH:
            return NORTH_ROOMS
        elif self.value == Direction.SOUTH:
            return SOUTH_ROOMS
        elif self.value == Direction.EAST:
            return EAST_ROOMS
        elif self.value == Direction.WEST:
            return WEST_ROOMS

    def cap(self):
        if self.value == Direction.NORTH:
            return NORTH_CAP
        elif self.value == Direction.SOUTH:
            return SOUTH_CAP
        elif self.value == Direction.EAST:
            return EAST_CAP
        elif self.value == Direction.WEST:
            return WEST_CAP


def generate_random_id(entity_type: EntityType):
    return entity_type.name + str(random.randint(1000, 9999))


def normalize(v):
    """
    Normalise a vector
    :param v: a vector
    :return: normalised vector
    """
    return v / np.linalg.norm(v)


def euclidean_distance(iter1, iter2):
    vector1 = normalize(np.fromiter(iter1, dtype=float))
    vector2 = normalize(np.fromiter(iter2, dtype=float))

    if np.array_equal(vector1, vector2):
        return 0.
    else:
        return np.linalg.norm(vector1 - vector2)


def cosine_similarity(iter1, iter2):
    vector1 = np.fromiter(iter1, dtype=float)
    vector2 = np.fromiter(iter2, dtype=float)
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
