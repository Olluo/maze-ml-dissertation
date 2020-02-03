ENEMY_LIMIT = 10

ENEMY_MIN_HEALTH = 1
ENEMY_MAX_HEALTH = 100
ENEMY_HEALTH_POINTS = 500

ENEMY_MIN_STRENGTH = 1
ENEMY_MAX_STRENGTH = 100
ENEMY_STRENGTH_POINTS = 500

ENEMY_MIN_TREASURE_DROP = 0
ENEMY_MAX_TREASURE_DROP = 2

class Treasure:
    def __init__(self, points: int):
        self.points = points

class Enemy:
    def __init__(self, available_health: int, available_strength: int, available_treasures: int):
        self.health = random.choice(
            range(ENEMY_MIN_HEALTH, (ENEMY_MAX_HEALTH if available_health > ENEMY_MAX_HEALTH else available_health)))
        self.strength = random.choice(
            range(ENEMY_MAX_STRENGTH,
                  (ENEMY_MAX_STRENGTH if available_strength > ENEMY_MAX_STRENGTH else available_strength)))
        self.treasures = []
        for treasure in random.choice(
                range(ENEMY_MIN_TREASURE_DROP, (
                ENEMY_MAX_TREASURE_DROP if available_treasures > ENEMY_MAX_TREASURE_DROP else available_treasures))):
            self.treasures.append(Treasure(10))
