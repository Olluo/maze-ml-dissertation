import json
import random
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List
import pprint

from math import sqrt

import networkx as nx


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


class NodeType(IntEnum):
    ENEMY = 0
    ROOM = 1
    DOOR = 2
    TREASURE = 3
    HEALTH = 4
    STRENGTH = 5
    PLAYER = 99


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


class DoorType(IntEnum):
    ARCH = 0
    # CLOSED = 1
    # LOCKED = 2
    # TRAPPED = 3
    # SECRET = 4
    # STAIRS_UP = 5
    # STAIRS_DOWN = 6
    BARRICADE = 7
    ENTRANCE = 8
    EXIT = 9

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

    def add_entrance(self, direction: Direction):
        self.add_connection(direction=direction, door_type=DoorType.ENTRANCE, connection_id=None)

    def add_exit(self, direction: Direction):
        self.add_connection(direction=direction, door_type=DoorType.EXIT, connection_id=None)

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

    def add_to_graph(self, graph: nx.Graph):
        graph.add_node(self.node_id, type=int(NodeType.ROOM), value=int(self.room_type))
        if self.north_door[0] in [DoorType.ARCH]:
            graph.add_edge(self.node_id, self.north_door[1], type=int(self.north_door[0]))
        elif self.north_door[0] in [DoorType.ENTRANCE, DoorType.EXIT]:
            graph.add_edge(self.node_id, str(self.north_door[0].name), type=int(self.north_door[0]))

        if self.south_door[0] in [DoorType.ARCH]:
            graph.add_edge(self.node_id, self.south_door[1], type=int(self.south_door[0]))
        elif self.south_door[0] in [DoorType.ENTRANCE, DoorType.EXIT]:
            graph.add_edge(self.node_id, str(self.south_door[0].name), type=int(self.south_door[0]))

        if self.east_door[0] in [DoorType.ARCH]:
            graph.add_edge(self.node_id, self.east_door[1], type=int(self.east_door[0]))
        elif self.east_door[0] in [DoorType.ENTRANCE, DoorType.EXIT]:
            graph.add_edge(self.node_id, str(self.east_door[0].name), type=int(self.east_door[0]))

        if self.west_door[0] in [DoorType.ARCH]:
            graph.add_edge(self.node_id, self.west_door[1], type=int(self.west_door[0]))
        elif self.west_door[0] in [DoorType.ENTRANCE, DoorType.EXIT]:
            graph.add_edge(self.node_id, str(self.west_door[0].name), type=int(self.west_door[0]))

    @staticmethod
    def connect_rooms(room1: 'Room', room2: 'Room', direction: Direction, door_type: DoorType):
        room1.add_connection(direction, door_type, room2.node_id)
        room2.add_connection(direction.opposite(), door_type, room1.node_id)

    def draw(self, display=False):
        room = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'N', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '|', '-', '-', '-', '-', '-', '-', '|', '|', '-', '-', '-', '-', '-', '-', '|', ' '],
            [' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' '],
            ['W', '=', ' ', ' ', ' ', 'R', 'O', 'O', 'M', '#', '#', '#', '#', ' ', ' ', ' ', '=', 'E'],
            [' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' '],
            [' ', '|', '-', '-', '-', '-', '-', '-', '|', '|', '-', '-', '-', '-', '-', '-', '|', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]
        room[0][8:10] = str(self.north_door[0].draw(Direction.NORTH))
        room[-1][8:10] = str(self.south_door[0].draw(Direction.SOUTH))
        room[3][0] = str(self.west_door[0].draw(Direction.WEST))
        room[3][-1] = str(self.east_door[0].draw(Direction.EAST))
        room[3][5:13] = list(self.node_id)

        if display:
            for x in room:
                print(x)

        return room


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
        graph = nx.Graph()
        for room in self.rooms:
            room.add_to_graph(graph)
        return graph

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
        dimension = int(sqrt(len(self.rooms)))
        level = []
        for i in range(dimension):
            group = [[], [], [], [], [], [], []]
            for j in range(dimension):
                index = i * dimension + j
                room = self.rooms[index].draw()
                group = [x[0] + x[1] for x in zip(group, room)]
            level = group + level

        for x in level:
            print(''.join(x))


def generate_level():
    return basic_level()


def basic_level():
    """ Returns a basic level for proof of concept """
    rooms = [Room(room_type=RoomType.ENTRANCE)] + [Room() for _ in range(7)] + [Room(room_type=RoomType.EXIT)]

    rooms[0].add_entrance(Direction.SOUTH)
    rooms[-1].add_exit(Direction.NORTH)

    Room.connect_rooms(rooms[0], rooms[1], Direction.EAST, DoorType.ARCH)
    Room.connect_rooms(rooms[1], rooms[2], Direction.EAST, DoorType.ARCH)

    Room.connect_rooms(rooms[2], rooms[5], Direction.NORTH, DoorType.ARCH)

    Room.connect_rooms(rooms[5], rooms[4], Direction.WEST, DoorType.ARCH)
    Room.connect_rooms(rooms[4], rooms[3], Direction.WEST, DoorType.ARCH)

    Room.connect_rooms(rooms[3], rooms[6], Direction.NORTH, DoorType.ARCH)

    Room.connect_rooms(rooms[6], rooms[7], Direction.EAST, DoorType.ARCH)
    Room.connect_rooms(rooms[7], rooms[8], Direction.EAST, DoorType.ARCH)

    # Room.connect_rooms(rooms[0], rooms[3], Direction.NORTH, DoorType.ARCH)

    return Level(rooms=rooms)


if __name__ == '__main__':
    level = generate_level()
    level.draw_level()
    graph = level.to_graph()
    nx.write_graphml(graph, 'test_graph.xml')

"""
        N                N                N        
 |======D======|  |======D======|  |======D======| 
 |             |  |             |  |             | 
WD   ROOM1234  DEWD   ROOM1234  DEWD   ROOM1234  DE
 |             |  |             |  |             | 
 |======D======|  |======D======|  |======D======| 
        S                S                S        
        N                N                N        
 |======D======|  |======D======|  |======D======| 
 |             |  |             |  |             | 
WD   ROOM1234  DEWD   ROOM1234  DEWD   ROOM1234  DE
 |             |  |             |  |             | 
 |======D======|  |======D======|  |======D======| 
        S                S                S        
        N                N                N        
 |======D======|  |======D======|  |======D======| 
 |             |  |             |  |             | 
WD   ROOM1234  DEWD   ROOM1234  DEWD   ROOM1234  DE
 |             |  |             |  |             | 
 |======D======|  |======D======|  |======D======| 
        S                S                S        
"""


