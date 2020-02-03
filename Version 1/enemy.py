from enum import IntEnum
import random
from typing import List

from constants import NodeType, generate_node_id
from treasure import Treasure


class Strength(IntEnum):
    WEAK = 0
    STRONG = 1


class Health(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


StrengthList = List[Strength]
HealthList = List[Health]


class Enemy:
    def __init__(self, graph, node_id: str, strength: Strength, health: Health):
        self.id = node_id
        self.graph = graph

        self.graph.add_node(self.id, type=int(NodeType.ENEMY), value=int(strength), value2=int(health))

    def add_treasure(self, treasure: Treasure):
        """ Add the treasure as a drop of killing the enemy """
        self.graph.add_edge(self.id, treasure.id)


def generate_enemies(graph, num_enemies, strengths: StrengthList, healths: HealthList):
    """
    Generate num_enemies enemies based on the strengths and healths in the 2 lists passed in.
    Returns a list of the node_ids of all the enemies
    """
    return [Enemy(graph=graph,
                  node_id=generate_node_id(node_type=NodeType.ENEMY),
                  strength=strengths[i],
                  health=healths[i])
            for i in range(num_enemies)]


def generate_strengths(num_enemies, strong_probability: float = 0.2) -> StrengthList:
    """
    Generate num_enemies random strengths
    :param num_enemies: The number of strengths to generate
    :param strong_probability: is the probability of choosing STRONG as the strength of the enemy
    """
    assert strong_probability < 1.0
    return random.choices(population=list(Strength), weights=[1 - strong_probability, strong_probability],
                          k=num_enemies)


def generate_healths(num_enemies, medium_probability: float = 0.4, high_probability: float = 0.2) -> HealthList:
    """
    Generate num_enemies random healths
    :param num_enemies: The number of healths to generate
    :param medium_probability: is the probability of choosing MEDIUM as the health of the enemy
    :param high_probability: is the probability of choosing HIGH as the health of the enemy
    """
    assert medium_probability + high_probability < 1.0
    return random.choices(population=list(Health),
                          weights=[1 - medium_probability - high_probability, medium_probability, high_probability],
                          k=num_enemies)
