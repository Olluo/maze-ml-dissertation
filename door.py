import random
from enum import IntEnum, auto

from utils import Direction, START_ROOM


class DoorType(IntEnum):
    ARCH = auto()
    # CLOSED = auto()
    # LOCKED = auto()
    # TRAPPED = auto()
    # SECRET = auto()
    # STAIRS_UP = auto()
    # STAIRS_DOWN = auto()
    BARRICADE = auto()

    def draw(self, direction: Direction):
        if self.value == DoorType.ARCH:
            return ' '
        elif self.value == DoorType.BARRICADE:
            return '║' if (direction == direction.EAST or direction == direction.WEST) else '═'


class DoorConfig:
    def __init__(self, north: bool, south: bool, east: bool, west: bool):
        """
        The configuration of the doors
        :param north: whether there is a north door in the room
        :param south: whether there is a south door in the room
        :param east: whether there is a east door in the room
        :param west: whether there is a west door in the room
        """
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    @property
    def raw(self):
        return [self.north, self.south, self.east, self.west]

    @staticmethod
    def random_config(direction: Direction) -> 'DoorConfig':
        """
        Return a random DoorConfig for a room that will be placed in direction
        """
        return DoorConfig(*random.choice(direction.rooms()))

    @staticmethod
    def cap(direction: Direction) -> 'DoorConfig':
        """
        Return the DoorConfig of the cap for the direction
        """
        return DoorConfig(*direction.cap())

    @staticmethod
    def start() -> 'DoorConfig':
        """
        Return the DoorConfig of the start room
        """
        return DoorConfig(*START_ROOM)


class Door:
    # TODO actually make barricades work
    def __init__(self, direction: Direction, door_type: DoorType = DoorType.ARCH):
        self.direction = direction
        self.type = door_type
        self.connection = None

    def draw(self):
        return self.type.draw(self.direction)

    @property
    def has_connection(self):
        return self.connection is not None
