import random
from statistics import mean, StatisticsError
from typing import Optional, List, Tuple

import networkx as nx

from constants import LEVEL_LAYOUT_DIMENSION, LEVEL_DEPTH_LIMIT, ENEMY_PROBABILITY, TREASURE_PROBABILITY, \
    LEVEL_EDGE_INDICES, ENEMY_MIN_NUMBER_PER_ROOM, ENEMY_MAX_NUMBER_PER_ROOM, LEVEL_MAX_NUMBER_OF_ROOMS
from door import DoorConfig
from enemy import Enemy, EnemyType
from room import Room, RoomType, BLANK_ROOM_ASCII
from treasure import Treasure, TreasureValue
from utils import Direction


class Level:
    def __init__(self):
        self.level_layout: List[List[Optional[Room]]] = [[None for _ in range(LEVEL_LAYOUT_DIMENSION)] for _ in
                                                         range(LEVEL_LAYOUT_DIMENSION)]
        self.rooms: List[Room] = []
        self.treasures: List[Treasure] = []
        self.enemies: List[Enemy] = []

        self.start_room: Optional['Room'] = None
        self.exit_room: Optional['Room'] = None

        self.generate_level()

    def generate_level(self):
        self.start_room = Room(DoorConfig.start(), room_type=RoomType.ENTRANCE)
        self.rooms.append(self.start_room)

        current_index = (LEVEL_DEPTH_LIMIT, LEVEL_DEPTH_LIMIT)
        self.level_layout[current_index[0]][current_index[1]] = self.start_room

        self.add_rooms(self.start_room, current_index)

        self.exit_room = self.rooms[-1]
        self.exit_room.make_exit()

    def add_rooms(self, room: Room, current_index, treasure_probability=TREASURE_PROBABILITY,
                  enemy_probability=ENEMY_PROBABILITY):
        x_index, y_index = current_index
        new_x_index, new_y_index = x_index, y_index

        connections_to_add: List[Direction] = room.unset_directions

        new_rooms: List[Tuple[Room, Tuple[int, int]]] = []
        for direction in connections_to_add:
            door_config = DoorConfig.cap(direction)

            if direction == Direction.NORTH:
                new_y_index -= 1
            elif direction == Direction.SOUTH:
                new_y_index += 1
            elif direction == Direction.EAST:
                new_x_index += 1
            elif direction == Direction.WEST:
                new_x_index -= 1

            if new_x_index in LEVEL_EDGE_INDICES or new_y_index in LEVEL_EDGE_INDICES:
                cap = True
            else:
                cap = False

            new_room = self.level_layout[new_y_index][new_x_index]
            if new_room is None:
                if cap:
                    new_room = Room(door_config)
                else:
                    new_room = Room.random_room(direction)

                if random.random() < treasure_probability:
                    treasure = Treasure.random_treasure()
                    self.treasures.append(treasure)
                    new_room.add_treasure(treasure)
                    treasure_probability = TREASURE_PROBABILITY
                else:
                    treasure_probability += TREASURE_PROBABILITY

                if random.random() < enemy_probability:
                    number_of_enemies = random.randint(ENEMY_MIN_NUMBER_PER_ROOM, ENEMY_MAX_NUMBER_PER_ROOM)
                    for _ in range(number_of_enemies):
                        enemy = Enemy.random_enemy()
                        self.enemies.append(enemy)
                        new_room.add_enemy(enemy)
                        enemy_probability = ENEMY_PROBABILITY
                else:
                    enemy_probability += ENEMY_PROBABILITY

                self.rooms.append(new_room)

            self._add_connection(room, new_room, direction)
            self.level_layout[new_y_index][new_x_index] = new_room

            if not cap:
                new_rooms.append((new_room, (new_x_index, new_y_index)))

            new_x_index, new_y_index = x_index, y_index

        for new_room, index in new_rooms:
            self.add_rooms(new_room, index, treasure_probability, enemy_probability)
        return

    def draw(self):
        dimension = LEVEL_LAYOUT_DIMENSION
        level = []
        for y in range(dimension):
            group = [[], [], []]
            for x in range(dimension):
                room = self.level_layout[y][x]
                if room is None:
                    room = BLANK_ROOM_ASCII
                else:
                    room = room.draw()
                group = [b[0] + b[1] for b in zip(group, room)]
            level = level + group

        for x in level:
            print(''.join(x))

    def to_graph(self):
        graph = nx.Graph()
        for room in self.rooms:
            room.add_to_graph(graph)
        return graph

    def to_vector(self):
        number_rooms = len(self.rooms) / LEVEL_MAX_NUMBER_OF_ROOMS
        number_1_connection_rooms = self.number_x_connection_rooms(1) / LEVEL_MAX_NUMBER_OF_ROOMS
        number_2_connection_rooms = self.number_x_connection_rooms(2) / LEVEL_MAX_NUMBER_OF_ROOMS
        number_3_connection_rooms = self.number_x_connection_rooms(3) / LEVEL_MAX_NUMBER_OF_ROOMS

        # could have treasure in every room but start room
        number_treasures = len(self.treasures) / (LEVEL_MAX_NUMBER_OF_ROOMS - 1)

        try:
            average_treasure_value = mean([int(treasure.value) for treasure in self.treasures]) / int(
                TreasureValue.HIGH)
        except StatisticsError:
            average_treasure_value = 0.

        # can have up to 3 enemies per room
        number_enemies = len(self.enemies) / ((LEVEL_MAX_NUMBER_OF_ROOMS - 1) * ENEMY_MAX_NUMBER_PER_ROOM)
        try:
            average_enemy_strength = mean([int(enemy.enemy_type) for enemy in self.enemies]) / int(EnemyType.STRONG)
        except StatisticsError:
            average_enemy_strength = 0.

        graph = self.to_graph()

        distance_start_exit = len(nx.shortest_path(graph, source=self.start_room.id, target=self.exit_room.id)) - 1

        distances_rooms_to_start = [len(nx.shortest_path(graph, source=self.start_room.id, target=room.id)) - 1 for room
                                    in self.rooms[1:]]
        distance_start_furthest = max(distances_rooms_to_start)

        distances_rooms_to_exit = [len(nx.shortest_path(graph, source=self.exit_room.id, target=room.id)) - 1 for room
                                   in self.rooms[:-1]]
        distance_exit_furthest = max(distances_rooms_to_exit)

        loc = locals()
        return dict([(i, loc[i]) for i in (
            "number_rooms",
            "number_1_connection_rooms",
            "number_2_connection_rooms",
            "number_3_connection_rooms",
            "number_treasures",
            "average_treasure_value",
            "number_enemies",
            "average_enemy_strength",
            "distance_start_exit",
            "distance_start_furthest",
            "distance_exit_furthest",
        )])

    def number_x_connection_rooms(self, number_of_connections: int):
        return len([room for room in self.rooms if room.number_of_connections == number_of_connections])

    @staticmethod
    def _add_connection(room1, room2, direction):
        room1.add_connection(room2, direction)
        room2.add_connection(room1, direction.opposite())

    @staticmethod
    def random_level_set(number_of_levels: int):
        return [Level() for _ in range(number_of_levels)]
