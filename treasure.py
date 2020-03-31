import random
from enum import auto, IntEnum

from utils import generate_random_id, EntityType


class TreasureValue(IntEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

    def draw(self):
        if self.value == TreasureValue.LOW:
            return '+'
        elif self.value == TreasureValue.MEDIUM:
            return '*'
        elif self.value == TreasureValue.HIGH:
            return '$'


class Treasure:
    def __init__(self, value: TreasureValue):
        self.value = value

        self.entity_type = EntityType.TREASURE
        self.id = generate_random_id(self.entity_type)

    @staticmethod
    def random_treasure() -> 'Treasure':
        return Treasure(random.choice(list(TreasureValue)))

    def draw(self):
        return self.value.draw()
