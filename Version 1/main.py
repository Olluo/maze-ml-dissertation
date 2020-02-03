"""
generate x amount of enemies each with a unique id
the ids for the health/strength nodes can be the id of the enemy with an h/s on the end
ids can be 5 digit numbers

need a room generator but may be a good idea to just have 10x10 rooms everytime and the connections are random
2 rooms will need to have type as entry room or exit room
rooms can be connected to up to 3 other rooms

treasures can either be in a room or as a result of killing an enemy
treasures are either small or big

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

"""

