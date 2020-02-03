import json
import random
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List


def generate_level():
    return basic_level()


def basic_level():
    """ Returns a basic level for proof of concept """


class EntityType(IntEnum):
    ENEMY = 0
    ROOM = 1
    TREASURE = 3
    PLAYER = 99


class RoomType(IntEnum):
    ENTRANCE = 0
    EXIT = 1
    # TREASURE = 2
    STANDARD = 3
    # CORRIDOR = 4


class DoorType(IntEnum):
    ARCH = 0
    # CLOSED = 1
    # LOCKED = 2
    # TRAPPED = 3
    # SECRET = 4
    # STAIRS_UP = 5
    # STAIRS_DOWN = 6
    BARRICADE = 7


class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    @staticmethod
    def opposite(direction):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        elif direction == Direction.SOUTH:
            return Direction.NORTH
        elif direction == Direction.EAST:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.EAST


def generate_random_id(entity_type: EntityType):
    return entity_type.name + str(random.randint(1000, 9999))


class Room:
    def __init__(self, room_type: RoomType = RoomType.STANDARD, north_door=None, south_door=None, east_door=None,
                 west_door=None, node_id: str = None):
        self.north_door = [DoorType.BARRICADE, None] if north_door is None else north_door
        self.south_door = [DoorType.BARRICADE, None] if south_door is None else south_door
        self.east_door = [DoorType.BARRICADE, None] if east_door is None else east_door
        self.west_door = [DoorType.BARRICADE, None] if west_door is None else west_door
        self.room_type = room_type
        self.node_id = node_id if node_id is not None else generate_random_id(EntityType.ROOM)

    def add_connection(self, direction: Direction, door_type: DoorType, connection_id):
        if direction == Direction.NORTH:
            self.north_door = [door_type, connection_id]
        elif direction == Direction.SOUTH:
            self.south_door = [door_type, connection_id]
        elif direction == Direction.EAST:
            self.east_door = [door_type, connection_id]
        elif direction == Direction.WEST:
            self.west_door = [door_type, connection_id]

    @staticmethod
    def from_dict(data):
        return Room(room_type=data['room_type'],
                    north_door=data['north_door'],
                    south_door=data['south_door'],
                    east_door=data['east_door'],
                    west_door=data['west_door'],
                    node_id=data['node_id']
                    )

    def to_dict(self):
        return {'room_type': self.room_type,
                'north_door': self.north_door,
                'south_door': self.south_door,
                'east_door': self.east_door,
                'west_door': self.west_door,
                'node_id': self.node_id
                }

    @staticmethod
    def connect_rooms(room1: 'Room', room2: 'Room', direction: Direction, door_type: DoorType):
        room1.add_connection(direction, door_type, room2.node_id)
        room2.add_connection(Direction.opposite(direction), door_type, room1.node_id)


class AbstractLevel(ABC):
    @abstractmethod
    def to_file(self, file_name: str = "level.csv"):
        pass

    @staticmethod
    @abstractmethod
    def from_file(file_name: str = "level.csv") -> 'AbstractLevel':
        pass

    @abstractmethod
    def to_graph(self):
        pass

    @staticmethod
    @abstractmethod
    def from_graph(graph) -> 'AbstractLevel':
        pass


class Level(AbstractLevel):
    """
    A level always has:
    - 9 rooms (3x3 grid)
        a room always has:
        - 4 doors (n, s, e, w)
            a door always has:
            - a type
        - a type
    - 1 entrance
    - 1 exit
    - a route through the level
    - all rooms connected
    """

    def __init__(self, rooms: List[Room]):
        self.rooms = rooms

    def to_file(self, file_name: str = "level.json"):
        pass

    @staticmethod
    def from_file(file_name: str = "level.json") -> 'Level':
        pass

    def to_graph(self):
        pass

    @staticmethod
    def from_graph(graph) -> 'Level':
        pass

    def to_dict(self):
        level = {}
        for room in self.rooms:
            level['rooms'].append(room.to_dict())
        return level

    @staticmethod
    def from_dict(graph) -> 'Level':
        pass

    def draw_level(self):
        room_top = """ |======D======|
 |             |"""
        west_wall = """W"""
        east_wall = """E"""
        room_middle = """D   ROOM#  D"""
        room_bottom = """ |             |
 |======D======|"""
        north_wall = """        N"""
        south_wall = """        S"""




level = {'rooms': []}
r1 = Room(room_type=RoomType.ENTRANCE)
r2 = Room()
r3 = Room()
r4 = Room()
r5 = Room()
r6 = Room()
r7 = Room()
r8 = Room()
r9 = Room(room_type=RoomType.EXIT)
rooms = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
Room.connect_rooms(r1, r2, Direction.EAST, DoorType.ARCH)
Room.connect_rooms(r2, r3, Direction.EAST, DoorType.ARCH)

Room.connect_rooms(r3, r4, Direction.NORTH, DoorType.ARCH)

Room.connect_rooms(r4, r5, Direction.WEST, DoorType.ARCH)
Room.connect_rooms(r5, r6, Direction.WEST, DoorType.ARCH)

Room.connect_rooms(r6, r7, Direction.NORTH, DoorType.ARCH)

Room.connect_rooms(r7, r8, Direction.EAST, DoorType.ARCH)
Room.connect_rooms(r8, r9, Direction.EAST, DoorType.ARCH)

for room in rooms:
    level['rooms'].append(room.to_dict())
print(level)

x = json.dumps(level)
print(x)

"""
        N
 |======D======|
 |             |
WD   ROOM#  DE
 |             |
 |======D======|
        S
"""


