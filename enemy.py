import random
from enum import IntEnum, auto

from utils import EntityType, generate_random_id


class EnemyType(IntEnum):
    WEAK = auto()
    STRONG = auto()

    def draw(self):
        if self.value == EnemyType.WEAK:
            return 'e'
        elif self.value == EnemyType.STRONG:
            return 'E'


class EnemyAttackType(IntEnum):
    MISS = auto()
    WEAK = auto()
    STRONG = auto()


class Enemy:
    def __init__(self, enemy_type: EnemyType):
        self.enemy_type = enemy_type

        self.entity_type = EntityType.ENEMY
        self.id = generate_random_id(self.entity_type)

        self.health = int(self.enemy_type)

    @staticmethod
    def random_enemy() -> 'Enemy':
        return Enemy(random.choice(list(EnemyType)))

    def draw(self):
        return self.enemy_type.draw()

    def kill(self):
        # damage = random.choices(list(EnemyAttackType),
        #                         weights=ENEMY_ATTACK_TYPE_PROBABILITIES_WEAK if (
        #                                 self.enemy_type == EnemyType.WEAK) else (
        #                             ENEMY_ATTACK_TYPE_PROBABILITIES_STRONG),
        #                         k=1)[0]
        # self.health -= 1
        # # player.damage(damage)
        # if self.health <= 0:
        return int(self.enemy_type)
