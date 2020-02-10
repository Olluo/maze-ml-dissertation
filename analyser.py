import time

import networkx as nx

from constants import Action, ActionType

PLAYER_DATA = {
    'rooms_visited': 0,
    'doors_opened': 0,
    'enemies_killed': 0,
    'points_collected': 0,
    'route': [],
    'start_time': 0,
    'end_time': 0
}


class Analyser:
    def __init__(self, level):
        self.data = {}
        self.level = level
        self.shortest_path = nx.shortest_path(level.to_graph(), source='ENTRANCE', target='EXIT')

    def register_player(self, player_id):
        self.data[player_id] = dict(PLAYER_DATA)

    def communicate(self, action: Action, player_id):
        try:
            ActionType(action.type)
        except NameError:
            print(f'ERROR: invalid action: {action}')

        if action.type == ActionType.START_LEVEL:
            self.data[player_id]['start_time'] = time.time()
        elif action.type == ActionType.END_LEVEL:
            self.data[player_id]['end_time'] = time.time()
        elif action.type == ActionType.ENTER_ROOM:
            self.data[player_id]['rooms_visited'] += 1
            self.data[player_id]['route'].append(action.data['room_id'])

    def calculate_player_type(self, player_id):
        return 'player_type_stub'

    def generate_new_level(self, player):
        pass
