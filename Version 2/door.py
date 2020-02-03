from constants import DoorType, EntityType, generate_random_id
from room import Room


class Door:
    def __init__(self, door_type: DoorType = DoorType.STANDARD):
        self.type = door_type
        self.node_id = generate_random_id(entity_type=EntityType.DOOR)
        self.entrance = None
        self.exit = None
        self.key = None

    def add_node_to_graph(self, graph, connections):
        pass

    def add_entrance(self, room: Room):
        self.entrance = room

    def add_exit(self, room: Room):
        self.exit = room

    def add_key(self, key: Treasure):
        self.key = key
