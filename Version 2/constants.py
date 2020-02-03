import random
from abc import ABC, abstractmethod
from enum import IntEnum


class AbstractNode(ABC):
    @abstractmethod
    def add_node_to_graph(self, graph, connections):
        pass


class EntityType(IntEnum):
    ENEMY = 0
    ROOM = 1
    DOOR = 2
    TREASURE = 3
    PLAYER = 99


class EnemyType(IntEnum):
    WEAK = 0
    MODERATE = 1
    STRONG = 2
    # WEAK_HIGH_HEALTH = 3
    # STRONG_LOW_HEALTH = 4
    # DECOY = 5


class RoomType(IntEnum):
    ENTRANCE = 0
    EXIT = 1
    TREASURE = 2
    STANDARD = 3
    CORRIDOR = 4


class DoorType(IntEnum):
    ARCH = 0
    CLOSED = 1
    LOCKED = 2
    # TRAPPED = 3
    # SECRET = 4
    # STAIRS_UP = 5
    # STAIRS_DOWN = 6


class TreasureType(IntEnum):
    INVALUABLE = 0
    MODERATE = 1
    VALUABLE = 2
    KEY = 3
    # WEAPON = 4
    # ARMOR = 5


def generate_random_id(entity_type: EntityType):
    return entity_type.name + str(random.randint(1000, 9999))

