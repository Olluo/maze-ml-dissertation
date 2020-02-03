from enum import IntEnum
from random import randint

ENEMY_LIMIT = 10

TREASURE_LIMIT = 10

ROOM_LIMIT = 10
DOOR_LIMIT = 3 * ROOM_LIMIT


class NodeType(IntEnum):
    ENEMY = 0
    ROOM = 1
    DOOR = 2
    TREASURE = 3
    HEALTH = 4
    STRENGTH = 5
    PLAYER = 99


def generate_node_id(node_type):
    letter = '0'
    if node_type == NodeType.ENEMY:
        letter = "E"
    elif node_type == NodeType.ROOM:
        letter = "R"
    elif node_type == NodeType.DOOR:
        letter = "D"
    elif node_type == NodeType.TREASURE:
        letter = "T"
    elif node_type == NodeType.PLAYER:
        letter = "P"

    return letter + str(randint(1000, 9999))

