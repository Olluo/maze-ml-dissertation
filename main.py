import pprint

import matplotlib.pyplot as plt
import numpy as np

from constants import NUMBER_PLAYERS, NUMBER_LEVELS
from level import Level
from player import Player, Personality
from utils import normalize, euclidean_distance


def main():
    players = Player.random_player_set(NUMBER_PLAYERS)

    # players = []
    # players.append(Player(Personality(0., 0., 0.)))
    # players.append(Player(Personality(1., 0., 0.)))
    # players.append(Player(Personality(0., 1., 0.)))
    # players.append(Player(Personality(0., 0., 1.)))
    # players.append(Player(Personality(1., 0., 1.)))
    # players.append(Player(Personality(0., 1., 1.)))
    # players.append(Player(Personality(1., 1., 0.)))
    # players.append(Player(Personality(1., 1., 1.)))
    # players.append(Player(Personality(1., 1., 1.)))

    player_vectors = []
    player_favourite_level_map = {}

    levels = Level.random_level_set(NUMBER_LEVELS)
    level_vectors = {level: level.to_vector() for level in levels}

    for player in players:
        player_vector, favourite_level = player.play_levels(levels, level_vectors)
        player_vectors.append(player_vector)
        player_favourite_level_map[player] = favourite_level

    # pprint.pprint(player_vectors)
    # pprint.pprint(level_vectors)
    # pprint.pprint(player_favourite_level_map)

    actual_player_vectors = [player.to_vector() for player in players]

    x_coordinates = []
    x2_coordinates = []
    y_coordinates = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            x = euclidean_distance(player_vectors[i].values(), player_vectors[j].values())
            x2 = euclidean_distance(actual_player_vectors[i].values(), actual_player_vectors[j].values())

            y = euclidean_distance(level_vectors[player_favourite_level_map[players[i]]].values(),
                                   level_vectors[player_favourite_level_map[players[j]]].values())

            x_coordinates.append(x)
            x2_coordinates.append(x2)
            y_coordinates.append(y)

    return x_coordinates, y_coordinates, x2_coordinates


if __name__ == "__main__":
    # player = Player(personality=Personality.random_personality())
    # level = Level()
    # level.draw()
    # pprint.pprint(level.to_vector())

    x_results, y_results, x2_results = main()

    plt.figure(figsize=(12, 4), dpi=800)
    plt.subplot(121)
    plt.scatter(x_results, y_results)
    plt.axis([-.2, np.sqrt(2), -.2, np.sqrt(2)])
    plt.subplot(122)
    plt.scatter(x2_results, y_results)
    plt.axis([-.2, np.sqrt(2), -.2, np.sqrt(2)])

    plt.suptitle('Scatter plot of similarities')
    plt.xlabel('Player Similarity')
    plt.ylabel('Level Similarity')
    plt.savefig('fig.png')

    # v1 = np.fromiter(vector_1.values(), dtype=float)
    # v2 = np.fromiter(vector_2.values(), dtype=float)
    #
    # similarity = 1 / np.linalg.norm(v1 - v2)
    # print(similarity)

    # g = lvl.to_graph()
    # nx.write_graphml(g, './test_graph.xml')
