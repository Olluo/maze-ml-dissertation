import random
from enum import IntEnum
from typing import List

from constants import NodeType, generate_node_id


class Type(IntEnum):
    OPEN = 0
    CLOSED = 1
    LOCKED = 2


TypeList = List[Type]


class Door:
    def __init__(self, graph, node_id: str, door_type: Type = Type.OPEN):
        self.id = node_id
        self.type = door_type
        self.graph = graph

        self.graph.add_node(self.id, type=int(NodeType.DOOR), value=int(door_type))


def generate_doors(graph, num_doors, num_rooms, values: TypeList):
    """
    """
    doors = []
    locked_doors = []
    num_doors = random.randint(num_rooms, num_doors)
    for i in range(num_doors):
        door = Door(graph=graph, node_id=generate_node_id(node_type=NodeType.DOOR), door_type=values[i])

        if door.type == Type.LOCKED:
            locked_doors.append(door)

        doors.append(door)

    return doors, locked_doors


def generate_door_states(num_doors, closed_probability: float = 0.4, locked_probability: float = 0.2) -> TypeList:
    """
    """
    assert closed_probability + locked_probability < 1.0
    return random.choices(population=list(Type),
                          weights=[1 - closed_probability - locked_probability, closed_probability, locked_probability],
                          k=num_doors)
