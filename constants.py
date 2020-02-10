import random
from collections import namedtuple
from enum import IntEnum, auto


class EntityType(IntEnum):
    ENEMY = auto()
    ROOM = auto()
    DOOR = auto()
    TREASURE = auto()
    PLAYER = auto()


class RoomType(IntEnum):
    ENTRANCE = auto()
    EXIT = auto()
    # TREASURE = auto()
    STANDARD = auto()
    # CORRIDOR = auto()


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


class ActionType(IntEnum):
    START_LEVEL = auto()
    END_LEVEL = auto()
    ENTER_ROOM = auto()
    EXIT_ROOM = auto()
    SCAN_DOOR = auto()
    KILL_ENEMY = auto()
    SATISFACTION = auto()


Action = namedtuple('Action', 'type, data')


class DoorType(IntEnum):
    ARCH = auto()
    # CLOSED = auto()
    # LOCKED = auto()
    # TRAPPED = auto()
    # SECRET = auto()
    # STAIRS_UP = auto()
    # STAIRS_DOWN = auto()
    BARRICADE = auto()
    ENTRANCE = auto()
    EXIT = auto()

    def draw(self, direction: Direction):
        if self.value == DoorType.ARCH:
            return '=' if (direction == direction.EAST or direction == direction.WEST) else '||'
        elif self.value == DoorType.BARRICADE:
            return '|' if (direction == direction.EAST or direction == direction.WEST) else '=='
        elif self.value == DoorType.ENTRANCE:
            return '*' if (direction == direction.EAST or direction == direction.WEST) else '**'
        elif self.value == DoorType.EXIT:
            return '&' if (direction == direction.EAST or direction == direction.WEST) else '&&'


def generate_random_id(entity_type: EntityType):
    return entity_type.name + str(random.randint(1000, 9999))
