import copy
from enum import IntEnum, auto
from typing import Optional, List

import networkx as nx

from constants import ENEMY_MAX_NUMBER_PER_ROOM
from door import DoorConfig, Door, DoorType
from enemy import Enemy
from treasure import Treasure
from utils import Direction, EntityType, generate_random_id

ROOM_ASCII = [
    ['█', '▀', '▀', '▀', '█'],
    ['█', ' ', ' ', ' ', '█'],
    ['█', '▄', '▄', '▄', '█'],
]

START_ROOM_ASCII = [
    ['╔', '═', '═', '═', '╗'],
    ['║', ' ', 'S', ' ', '║'],
    ['╚', '═', '═', '═', '╝'],
]

EXIT_ROOM_ASCII = [
    ['╔', '═', '═', '═', '╗'],
    ['║', ' ', 'X', ' ', '║'],
    ['╚', '═', '═', '═', '╝'],
]

BLANK_ROOM_ASCII = [
    ['░', '░', '░', '░', '░'],
    ['░', '░', '░', '░', '░'],
    ['░', '░', '░', '░', '░'],
]


class Action(IntEnum):
    COLLECT_TREASURE = auto()
    KILL_ENEMY = auto()


class RoomType(IntEnum):
    ENTRANCE = auto()
    EXIT = auto()
    # TREASURE = auto()
    STANDARD = auto()
    # CORRIDOR = auto()


class Room:
    def __init__(self, door_config: DoorConfig, room_type: RoomType = RoomType.STANDARD):
        self.north_door: Optional[Door] = Door(Direction.NORTH) if door_config.north else None
        self.south_door: Optional[Door] = Door(Direction.SOUTH) if door_config.south else None
        self.east_door: Optional[Door] = Door(Direction.EAST) if door_config.east else None
        self.west_door: Optional[Door] = Door(Direction.WEST) if door_config.west else None

        self.door_map = {
            Direction.NORTH: self.north_door,
            Direction.SOUTH: self.south_door,
            Direction.EAST: self.east_door,
            Direction.WEST: self.west_door
        }

        self.number_of_connections = sum(door_config.raw)

        self.treasure: Optional[Treasure] = None

        self.enemies: List[Enemy] = []

        self.type = room_type
        self.entity_type = EntityType.ROOM
        self.id = generate_random_id(self.entity_type)

        self.visited = False

    def add_connection(self, room: 'Room', direction: Direction):
        door = Door(direction, DoorType.BARRICADE) if self.door_map[direction] is None else self.door_map[direction]
        door.connection = room
        if room.door_map[direction.opposite()] is None:
            door.type = DoorType.BARRICADE

    @property
    def unset_directions(self):
        return [direction for direction, door in self.door_map.items() if door is not None and not door.has_connection]

    @property
    def set_directions(self):
        return [direction for direction, door in self.door_map.items() if door is not None and door.has_connection]

    @property
    def connections(self):
        return [door.connection for door in self.door_map.values() if
                door is not None and door.has_connection and door.type != DoorType.BARRICADE]

    def draw(self, display=False):
        if self.type == RoomType.ENTRANCE:
            room = copy.deepcopy(START_ROOM_ASCII)
        elif self.type == RoomType.EXIT:
            room = copy.deepcopy(EXIT_ROOM_ASCII)
        else:
            room = copy.deepcopy(ROOM_ASCII)

        if self.north_door:
            room[0][2] = self.north_door.draw()

        if self.south_door:
            room[2][2] = self.south_door.draw()

        if self.east_door:
            room[1][4] = self.east_door.draw()

        if self.west_door:
            room[1][0] = self.west_door.draw()

        if self.treasure is not None:
            room[1][1] = self.treasure.draw()

        if self.enemies:
            room[1][3] = str(len(self.enemies))

        if self.visited:
            room[1][2] = '■'

        if display:
            for x in room:
                print(''.join(x))

        return room

    def make_exit(self):
        self.type = RoomType.EXIT

    def add_to_graph(self, graph: nx.Graph):
        # Add this room to the graph
        graph.add_node(self.id, type=int(self.entity_type), value=int(self.type))

        for door in self.door_map.values():
            if door and door.type != DoorType.BARRICADE:
                graph.add_edge(self.id, door.connection.id, type=int(door.type))

        if self.treasure is not None:
            graph.add_node(self.treasure.id, type=int(self.treasure.entity_type), value=int(self.treasure.value))
            graph.add_edge(self.id, self.treasure.id)

        for enemy in self.enemies:
            graph.add_node(enemy.id, type=int(enemy.entity_type), value=int(enemy.enemy_type))
            graph.add_edge(self.id, enemy.id)

    def add_treasure(self, treasure: Treasure):
        if self.treasure is None:
            self.treasure = treasure
        else:
            raise ValueError('treasure already set')

    def add_enemy(self, enemy: Enemy):
        if len(self.enemies) < ENEMY_MAX_NUMBER_PER_ROOM:
            self.enemies.append(enemy)
        else:
            raise ValueError('enemies already set')

    @staticmethod
    def random_room(direction: Direction) -> 'Room':
        return Room(DoorConfig.random_config(direction))

    def get_actions(self) -> List[Action]:
        """
        :return: List of actions that the player could do in the room
        """
        actions = []
        if self.treasure:
            actions.append(Action.COLLECT_TREASURE)

        for _ in self.enemies:
            actions.append(Action.KILL_ENEMY)

        return actions

    def set_visited(self):
        self.visited = True
