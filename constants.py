LEVEL_DEPTH_LIMIT = 9  # This is the maximum distance in units that a room can be from the start room
LEVEL_LAYOUT_DIMENSION = 2 * LEVEL_DEPTH_LIMIT + 1
LEVEL_EDGE_INDICES = [0, LEVEL_LAYOUT_DIMENSION - 1]
LEVEL_MAX_NUMBER_OF_ROOMS = LEVEL_LAYOUT_DIMENSION**2

TREASURE_PROBABILITY = 0.1  # Probability of a room having a treasure in it

ENEMY_PROBABILITY = 0.3  # Probability of a room having at least ENEMY_MIN_NUMBER_PER_ROOM in it
ENEMY_MIN_NUMBER_PER_ROOM = 1  # The minimum number of enemies to spawn in a room if it is chosen to have an enemy in
ENEMY_MAX_NUMBER_PER_ROOM = 3  # The maximum number of enemies to spawn in a room if it is chosen to have an enemy in
ENEMY_ATTACK_TYPE_PROBABILITIES_WEAK = [0.4, 0.4, 0.2]
ENEMY_ATTACK_TYPE_PROBABILITIES_STRONG = [0.2, 0.4, 0.4]

# How much a good or bad event effects the patience of the player
PLAYER_GOOD_EXPERIENCE_MULTIPLIER = 0.05
PLAYER_BAD_EXPERIENCE_MULTIPLIER = 0.05

# The patience of the player to start (between 0 and 1)
PLAYER_START_PATIENCE = 0.5

NUMBER_LEVELS = 100
NUMBER_PLAYERS = 100
