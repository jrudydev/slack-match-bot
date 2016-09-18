#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The tree object replicates a trounmanet bracket. The height
# is set depeding on the number of players. The size will double to 
# accommodate any number of players with an even distribution.

from match import Match
from player import Player
import random

class TournyNode(object):
  '''
  Each node contains a key that will be used to equally distribute
  the users across the leaves of the tree. It also holds another object,
  in this case a match.
  '''

  def __init__(self, key):
    self.key = key
    self.match = None
    self.left = None
    self.right = None

  def __str__(self):
    return str(self.key)
 
  def __repr__(self):
    return str(self.key)


class TournyTree(object):
  '''
  The tree is initializes with a list of players and generates all the
  games of the tournament with the root node containing the championship game.
  '''

  def __init__(self):
    self.node = None
    self.__games = []
    self.__round = -1
    self.__height = -1

  def __set_height(self, players):
    '''
    Caculate the height of the tree based on the number of players
    '''
    height = 1
    bracket_size = 2
    while bracket_size < players:
      bracket_size *= 2
      height += 1

    self.__height = height

  def insert_matches(self, key, count, players, is_random):
    '''
    Generates the tree of empty matches starting at the root node and
    adding players at the leaves.
    '''
    n = TournyNode(key)
    if not self.node:
      self.node = n
      self.node.left = TournyTree()
      self.node.right = TournyTree()
      self.node.match = Match()
      
      if count > 1:
        # non leaf nodes have an empty match object inserted to them
        half = key / 2
        self.node.right.insert_matches(half, count - 1, players, is_random)

        if key % 2 == 1: half += 1
        self.node.left.insert_matches(half, count - 1, players, is_random)
      else:
        # leaf node reached so add one or two players to the game
        for x in range(self.node.key):
          if is_random:
            # pop a random player
            number_of_players = len(players)
            index = random.choice(range(number_of_players))
            random_player = players[index]
          else:
            index = 0
            random_player = players[index]
          
          del players[index]

          self.node.match.add_side(random_player)

  def get_games(self):
    return self.__games

  def __traverse_all_nodes(self):
    '''
    Traverse tree in order and return a row at the depth provided.
    '''
    result = []

    if not self.node:
      return result

    result.extend(self.node.left.__traverse_all_nodes())
    result.append(self.node)
    result.extend(self.node.right.__traverse_all_nodes())

    return result

  def __traverse_nodes(self, depth):
    '''
    Traverse tree in order and return a row at the depth provided.
    '''
    result = []

    if not self.node:
      return result

    result.extend(self.node.left.__traverse_nodes(depth - 1))
    if depth == 1:
      result.append(self.node)
    result.extend(self.node.right.__traverse_nodes(depth - 1))

    return result

  def __load_round_nodes(self):
    '''
    Return a list of nodes that correspond to the current round.
    '''
    nodes = []
    if self.__height != -1:
      adjusted_round = self.__round - 1
      depth = self.__height - adjusted_round
      nodes = self.__traverse_nodes(depth)
    else:
      print "The tree has not been initialized."
    
    return nodes

  def __load_round_matches(self):
    '''
    Return a list of matches that correspond to the current round.
    '''
    matches = []
    if self.__height != -1:
      adjusted_round = self.__round - 1
      depth = self.__height - adjusted_round
      nodes = self.__traverse_nodes(depth)

      for x in range(len(nodes)):
        matches.append(nodes[x].match)
    else:
      print "The tree has not been initialized."

    return matches

  def __create_round(self):
    '''
    Assign the match ids to the players before every round.
    '''
    self.__games = self.__load_round_matches()
    for x in range(len(self.__games)):
      self.__games[x].set_match_ids(x)

  def __promote_winners(self):
    '''
    Draw the winners from the previous round to populate the current one.
    '''
    for node in self.__load_round_nodes():
      node.match.add_side(node.left.node.match.get_winner())
      node.match.add_side(node.right.node.match.get_winner())

  def generate(self, slots, random):
    '''
    Initalize and reset the tree with the players provided.
    '''
    number_of_slots = len(slots)
    
    self.__round = 1
    self.node = None
    self.__set_height(number_of_slots)
    self.insert_matches(number_of_slots, self.__height, slots, random)

    self.__create_round()
  
  def advance(self):
    '''
    Try to adavance to the next round and promote the winners.
    '''
    response = ""
    if len(self.__games) != 1:
      self.__round += 1
      self.__promote_winners()
      self.__create_round()

      response = "Tournament bracket advanced to next round."
    else:
      response = "Tournament is over."

    return response

  def destroy(self):
    del self.__games[:]
    self.__round = -1
    self.__height = -1

    nodes = self.__traverse_all_nodes()
    del nodes[:]


if __name__ == '__main__':
  tree = TournyTree()
  first_player = Player("U555", "jru", "ru", "go")

  players = [
    first_player,
    Player("U123", "abc", "fabc", "labc"), 
    Player("U456", "def", "fdef", "ldef"), 
    Player("U789", "efg", "fefg", "lefg")]
  tree.generate(players)

  games = tree.get_games()
  for match in games:
    print match.get_score()

  games[first_player.get_match_id()].add_win("U555")

  games = tree.get_games()
  for match in games:
    print match.get_score()