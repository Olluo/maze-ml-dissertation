import networkx as nx

import enemy
import room
import door
import treasure

from constants import ENEMY_LIMIT, TREASURE_LIMIT, ROOM_LIMIT, DOOR_LIMIT


def generate_level(num_enemies: int = ENEMY_LIMIT, num_treasures: int = TREASURE_LIMIT, num_rooms: int = ROOM_LIMIT,
                   num_doors: int = DOOR_LIMIT):
    """ Generate a graph based on parameters """
    graph = nx.Graph()

    # generate items in maze
    rooms = room.generate_rooms(graph, num_rooms)

    enemies = enemy.generate_enemies(graph, num_enemies,
                                     enemy.generate_strengths(num_enemies), enemy.generate_healths(num_enemies))

    treasures = treasure.generate_treasures(graph, num_treasures,
                                            treasure.generate_values(num_treasures))

    doors, locked_doors = door.generate_doors(graph, num_doors, len(rooms),
                                              door.generate_door_states(num_doors))

    keys = treasure.generate_keys(graph, locked_doors,
                                  treasure.generate_values(len(locked_doors)))

    # randomly distribute enemies across rooms
    room.distribute_enemies(rooms, enemies)

    # generate connections between rooms
    room.generate_connections(graph, rooms, doors)

    # randomly distribute treasures across rooms
    room.distribute_treasures(rooms, treasures)

    # distribute keys around enemies
    room.distribute_keys(rooms, enemies, keys)

    # Check graph is completable
    verify_graph(graph)

    nx.write_graphml(graph, 'test_graph.xml')


def verify_graph(graph):
    pass
