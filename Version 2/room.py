import random
from typing import List

from constants import RoomType, EntityType, generate_random_id, DoorType
from door import Door


class Room:
    def __init__(self, room_type: RoomType = RoomType.STANDARD):
        self.type = room_type
        self.node_id = generate_random_id(entity_type=EntityType.ROOM)
        self.max_connections = random.randint(1, 3)
        self.connections = []
        self.enemies = []
        self.treasures = []

    def add_node_to_graph(self, graph, connections):
        pass

    def add_connection_to_room(self, connection_type: DoorType, connecting_room: 'Room'):
        if self.number_of_connections < self.max_connections and (connecting_room.number_of_connections <
                                                                  connecting_room.max_connections):
            connection = Door(connection_type)
            connection.add_entrance(self)
            connection.add_exit(connecting_room)
            self.connections.append(connection)
            connecting_room.connections.append(connection)

    def add_enemy_to_room(self, enemy: Enemy):
        self.enemies.append(enemy)

    def add_enemies_to_room(self, enemies: List[Enemy]):
        for enemy in enemies:
            self.add_enemy_to_room(enemy)

    def add_treasure_to_room(self, treasure: Treasure):
        self.treasures.append(treasure)

    def add_treasures_to_room(self, treasures: List[Treasure]):
        for treasure in treasures:
            self.add_treasure_to_room(treasure)

    @property
    def number_of_connections(self):
        return len(self.connections)

    @property
    def number_of_enemies(self):
        return len(self.enemies)

    @property
    def number_of_treasures(self):
        return len(self.treasures)
