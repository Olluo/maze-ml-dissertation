from analyser import Analyser
from constants import EntityType, generate_random_id, Action, ActionType
from level import Level


class Player:
    def __init__(self, speed: float = 1.0):
        self.node_type = EntityType.PLAYER
        self.speed = speed
        self.node_id = generate_random_id(self.node_type)

    def play_level(self, level: Level, analyser: Analyser, verbose=False):
        graph = level.to_graph()
        visited_nodes = []

        current_node = 'ENTRANCE'
        analyser.communicate(Action(ActionType.START_LEVEL), {})

        while current_node != 'EXIT':

            neighbours = graph.neighbours(current_node)
            next_step = neighbours[0]



        satisfaction = 1.0

