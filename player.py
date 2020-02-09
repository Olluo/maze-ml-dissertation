from analyser import Analyser
from level import Level


class Player:
    def __init__(self, speed: float = 1.0):
        self.speed = speed

    def play_level(self, level: Level, analyser: Analyser):
        graph_representation = level.to_graph()

        # play level
        # communicate with the analyser
        satisfaction = 1.0
        return satisfaction

