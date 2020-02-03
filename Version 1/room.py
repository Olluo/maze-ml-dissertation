import random
from enum import IntEnum

from constants import NodeType, generate_node_id
from enemy import Enemy
from treasure import Treasure


class Type(IntEnum):
    ENTRY = 0
    EXIT = 1
    STANDARD = 2


class Room:
    def __init__(self, graph, node_id: str, room_type: Type = Type.STANDARD):
        self.id = node_id
        self.graph = graph

        self.graph.add_node(self.id, type=int(NodeType.ROOM), value=int(room_type))

    def add_enemy(self, enemy: Enemy):
        """ Adds the enemy to this room """
        self.graph.add_edge(self.id, enemy.id)

    def add_treasure(self, treasure: Treasure):
        """ Adds the treasure to this room """
        self.graph.add_edge(self.id, treasure.id)


def generate_rooms(graph, num_rooms):
    # Add start and exit rooms
    rooms = [Room(graph=graph, node_id=generate_node_id(node_type=NodeType.ROOM), room_type=Type.ENTRY),
                    Room(graph=graph, node_id=generate_node_id(node_type=NodeType.ROOM), room_type=Type.EXIT)]

    # Add other rooms
    for i in range(num_rooms - 2):
        rooms.append(Room(graph=graph, node_id=generate_node_id(node_type=NodeType.ROOM)))

    return rooms


def distribute_enemies(rooms, enemies):
    # shuffle list??
    # random.shuffle(enemy_ids)
    while len(enemies) > 0:
        for room in rooms:
            number_to_add = random.randint(0, (2 if len(enemies) > 2 else len(enemies)))
            for _ in range(number_to_add):
                room.add_enemy(enemies.pop())


def distribute_treasures(room_ids, treasure_ids):
    return None


def distribute_keys(room_ids, enemy_ids, key_ids):
    return None


def generate_connections(graph, r, d):
    rooms = list(r)
    doors = list(d)
    random.shuffle(rooms)
    random.shuffle(doors)

    for index, room in enumerate(rooms):
        room_two_index = index + 1
        if room_two_index == len(rooms):
            room_two_index = 0

        door = doors.pop()

        graph.add_edges_from([(room.id, door.id), (door.id, rooms[room_two_index].id)])

    for door in doors:
        room1, room2 = random.sample(rooms, 2)
        graph.add_edges_from([(room1.id, door.id), (door.id, room2.id)])
