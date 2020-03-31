"""
Ideas:

player needs health - 100
enemy takes number of hits to kill based on strength level
each attack injures player by a value corresponding to the enemy

player goes into room, sees there are enemies so leaves way he came and may come back later
player goes into room, sees enemies and tries to run for an exit

player who just wants to get high score as soon as possible


treasures can either be in a room or as a result of killing an enemy
could add speed to enemies
could add powerups

write up of notes:

individual modules
in and output for each
discrete labels?
discrete distribution
have player memoru of doors visited and enemies
memory of your inventory this means could add keys to unlock doors
only move rooms around to begin with - keep everything in each room the same and see wheteher moving a roomhas an affect
distribute enemies randomly
try to keep it simple
measure the percentage of happiness of the player for a certain graph
try to generate an inexpensive mapping between the graph and the happiness
using a grid representation for the level will help with representatiom
its hard to make new graphs from old ones
make sure to do parallel working

breaking a barricade loses health gains points

escapist:
    - doesn't want to kill enemies
    - doesnt want to get treasures
    -just wants to find exit

    0.1, 0.1, 0.8

achiever:
    - prefers getting treasures
    - will kill enemies if easy to do so
    - wants to find exit with most amount of points they can

    0.5, 0.2, 0.3

explorer:
    - doesn't care about treasures
    - doesnt care about enemies
    - wants to go in as many rooms as possible so wont exit until satisfied

    0.1, 0.1, 0.8

killer:
    - doesnt care about treasures
    - will kill as many enemies as possible
    - then find exit

    0.1, 0.7, 0.2
"""
import random
import time
from typing import Optional, List

from constants import PLAYER_GOOD_EXPERIENCE_MULTIPLIER, PLAYER_BAD_EXPERIENCE_MULTIPLIER, PLAYER_START_PATIENCE
from enemy import Enemy
from level import Level
from room import Room, RoomType, Action


class Personality:
    def __init__(self, achiever_preference: float, explorer_preference: float, killer_preference: float):
        # Has to be between 0 and 1
        self.achiever_preference = min(max(achiever_preference, 0.), 1.)
        self.explorer_preference = min(max(explorer_preference, 0.), 1.)
        self.killer_preference = min(max(killer_preference, 0.), 1.)
        self.escapist_preference = 1. - (self.achiever_preference * self.explorer_preference * self.killer_preference)

    @staticmethod
    def random_personality():
        return Personality(*[random.random() for _ in range(3)])

    def __repr__(self):
        return str(self.to_vector())

    def to_vector(self):
        return {
            'achiever': self.achiever_preference,
            'escapist': self.escapist_preference,
            'explorer': self.explorer_preference,
            'killer': self.killer_preference,
        }


class Player:
    def __init__(self, personality: Personality):
        self.display: bool = False
        self.visited_nodes = []
        self.previous_room_connections: int = 0
        self.finished_level: bool = False
        self.got_bored: bool = False
        self.current_level: Optional[Level] = None

        self.patience: float = PLAYER_START_PATIENCE

        self.personality: Personality = personality

        self.enemies_killed: int = 0
        self.treasures_collected: int = 0

    def play(self, level: Level, display: bool = False):
        self.display = display
        self.current_level = level
        self.visited_nodes = []
        self.finished_level = False
        self.got_bored = False

        self.enemies_killed = 0
        self.treasures_collected = 0

        room = self.current_level.start_room
        self._play(room)
        return self.stats()

    def _play(self, room: Room):
        self.visited_nodes.append(room.id)

        room.set_visited()
        if self.display:
            print("\n" * 100)
            print(self.stats())
            self.current_level.draw()
            time.sleep(0.1)

        # get actions on room
        actions = room.get_actions()

        # Explorer likes rooms to be different and the maze to be long so for every room in a row that is the same
        # patience gets worse, every time there is a new room patience goes up, when exit found, the number of rooms
        # visited goes into the rating maybe
        if room.number_of_connections == self.previous_room_connections:
            self.bad_experience(self.personality.explorer_preference)
        else:
            self.good_experience(self.personality.explorer_preference)

        if room.type == RoomType.EXIT:
            self.do_actions(actions, room, do_all=True)
            self.finished_level = True
            self.end_experience()
            return
        else:
            self.do_actions(actions, room)

        if self.patience < 0.:
            # The more impatient they get, the higher change of them quitting
            if random.random() < self.patience * -1.:
                self.got_bored = True
                return

        connections = room.connections
        random.shuffle(connections)
        for connection in connections:
            if connection.id not in self.visited_nodes:
                self._play(connection)

            if self.finished_level or self.got_bored:
                return

    def stats(self):
        return {
            'rating': self.get_rating(),
            'killed_enemies': self.enemies_killed,
            'collected_treasures': self.treasures_collected,
            'visited_rooms': len(self.visited_nodes),
            'finished_level': self.finished_level,
        }

    def get_rating(self):
        if self.patience <= 0.:
            return 0.
        return self.patience

    def good_experience(self, multiplier):
        experience = multiplier * PLAYER_GOOD_EXPERIENCE_MULTIPLIER
        self.patience = min(self.patience + experience, 1.)

    def bad_experience(self, multiplier):
        experience = multiplier * PLAYER_BAD_EXPERIENCE_MULTIPLIER
        self.patience = max(self.patience - experience, -1.)

    def end_experience(self):
        visited_percentage = len(self.visited_nodes) / len(self.current_level.rooms)
        weighted_experience = visited_percentage * 2 - 1.
        weighted_experience *= self.personality.explorer_preference

        if weighted_experience > 0.:
            self.patience = min(self.patience + weighted_experience, 1.)
        elif weighted_experience < 0.:
            self.patience = max(self.patience + weighted_experience, -1.)

    def do_actions(self, actions: List[Action], room: Room, do_all: bool = False):
        random.shuffle(actions)

        if Action.COLLECT_TREASURE not in actions:
            self.bad_experience(self.personality.achiever_preference)

        if Action.KILL_ENEMY not in actions:
            self.bad_experience(self.personality.killer_preference)

        for action in actions:
            if action == Action.COLLECT_TREASURE:
                if random.random() < self.personality.achiever_preference or do_all:
                    self.collect_treasure(room)
                    self.good_experience(self.personality.achiever_preference)

            elif action == Action.KILL_ENEMY:
                if random.random() < self.personality.killer_preference or do_all:
                    self.kill_enemy(room.enemies[0], room)
                    self.good_experience(self.personality.killer_preference)

    def kill_enemy(self, enemy: Enemy, room: Room):
        enemy.kill()
        room.enemies.remove(enemy)
        self.enemies_killed += 1

    def collect_treasure(self, room: Room):
        # self.satisfaction += int(room.treasure.value)
        self.treasures_collected += 1
        room.treasure = None

    @staticmethod
    def random_player_set(number_of_players: int):
        return [Player(Personality.random_personality()) for _ in range(number_of_players)]

    def play_levels(self, levels, level_vectors):
        """ Returns player vector and favourite level """
        running_stats = {
            'total_enemies': 0,
            'total_treasures': 0,
            'total_rooms': 0,
            'killed_enemies': 0,
            'collected_treasures': 0,
            'visited_rooms': 0,
            'finished_levels': 0,
        }

        ratings = {}

        for level in levels:
            vector = level_vectors[level]
            running_stats['total_enemies'] += vector['number_enemies']
            running_stats['total_treasures'] += vector['number_treasures']
            running_stats['total_rooms'] += vector['number_rooms']

            stats = self.play(level)
            running_stats['killed_enemies'] += stats['killed_enemies']
            running_stats['collected_treasures'] += stats['collected_treasures']
            running_stats['visited_rooms'] += stats['visited_rooms']
            running_stats['finished_levels'] += int(stats['finished_level'])

            ratings[level] = stats['rating']

        try:
            killed_enemy_percentage = running_stats['killed_enemies'] / running_stats['total_enemies']
        except ZeroDivisionError:
            killed_enemy_percentage = 0.

        try:
            collected_treasure_percentage = running_stats['collected_treasures'] / running_stats['total_treasures']
        except ZeroDivisionError:
            collected_treasure_percentage = 0.

        try:
            visited_room_percentage = running_stats['visited_rooms'] / running_stats['total_rooms']
        except ZeroDivisionError:
            visited_room_percentage = 0.

        finished_level_percentage = running_stats['finished_levels'] / 100.

        loc = locals()
        return dict([(i, loc[i]) for i in (
            'killed_enemy_percentage',
            'collected_treasure_percentage',
            'visited_room_percentage',
            'finished_level_percentage',
        )]), max(ratings, key=ratings.get)

    def to_vector(self):
        return self.personality.to_vector()
