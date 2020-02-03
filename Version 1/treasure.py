import random
from enum import IntEnum
from typing import List

from constants import NodeType, generate_node_id


class Value(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Type(IntEnum):
    LOOT = 0
    KEY = 1


class InvalidTreasureConfigurationException(Exception):
    pass


ValueList = List[Value]


class Treasure:
    def __init__(self, graph, node_id: str, value: Value, treasure_type: Type = Type.LOOT, door_id: str = "None"):
        self.id = node_id
        self.graph = graph

        if treasure_type == Type.LOOT and door_id != "None":
            raise InvalidTreasureConfigurationException("door_id is not used when Type is not KEY!")
        elif treasure_type == Type.KEY and door_id == "None":
            raise InvalidTreasureConfigurationException("If treasure type is set to KEY a door_id must be provided!")

        self.value = value
        self.type = treasure_type
        self.door_id = door_id
        self.graph.add_node(self.id, type=int(NodeType.TREASURE), value=int(self.value), value2=int(self.type))

        if self.type == Type.KEY:
            self.graph.add_edge(self.id, door_id)


def generate_treasures(graph, num_treasures, values: ValueList):
    """
    """
    return [Treasure(graph=graph,
                     node_id=generate_node_id(node_type=NodeType.TREASURE),
                     value=values[i])
            for i in range(num_treasures)]


def generate_keys(graph, locked_doors, values: ValueList):
    """
    """
    return [Treasure(graph=graph,
                     node_id=generate_node_id(node_type=NodeType.TREASURE),
                     value=values[i],
                     treasure_type=Type.KEY,
                     door_id=locked_doors[i].id)
            for i in range(len(locked_doors))]


def generate_values(num_treasures, medium_probability: float = 0.4, high_probability: float = 0.2) -> ValueList:
    """
    """
    assert medium_probability + high_probability < 1.0
    return random.choices(population=list(Value),
                          weights=[1 - medium_probability - high_probability, medium_probability, high_probability],
                          k=num_treasures)
