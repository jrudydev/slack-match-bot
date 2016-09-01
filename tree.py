#!/usr/bin/python

from match import Match
from player import Player
import random

class TournyNode(object):
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
  def __init__(self):
    self.node = None
    self.__players = {}
    self.__games = []
    self.__round = -1
    self.__height = -1

  def __set_height(self, players):
    height = 1
    bracket_size = 2
    while bracket_size < players:
      bracket_size *= 2
      height += 1

    self.__height = height

  def insert_matches(self, key, count, players):
    n = TournyNode(key)
    if not self.node:
      self.node = n
      self.node.left = TournyTree()
      self.node.right = TournyTree()
      self.node.match = Match()
      
      if count > 1:
        half = key / 2
        self.node.right.insert_matches(half, count - 1, players)

        if key % 2 == 1: half += 1
        self.node.left.insert_matches(half, count - 1, players)
      else:
        for x in range(self.node.key):
          # pop a random player
          number_of_players = len(players)
          if number_of_players == 0:
            return None

          rand_int = random.choice(range(number_of_players))
          random_player = players[rand_int]
          del players[rand_int]

          self.node.match.add_side(random_player)

  def get_games(self):
    return self.__games

  def __traverse_nodes(self, round_number):
    result = []

    if not self.node:
      return result

    result.extend(self.node.left.__traverse_nodes(round_number - 1))
    if round_number == 1:
      result.append(self.node)
    result.extend(self.node.right.__traverse_nodes(round_number - 1))

    return result

  def __load_round_nodes(self):
    nodes = []
    if self.__height != -1:
      adjusted_round = self.__round - 1
      depth = self.__height - adjusted_round
      nodes = self.__traverse_nodes(depth)
    else:
      print "The tree has not been initialized."
    
    return nodes

  def __load_round_matches(self):
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
    self.__games = self.__load_round_matches()
    for x in range(len(self.__games)):
      self.__games[x].set_match_ids(x)

  def __promote_winners(self):
    for node in self.__load_round_nodes():
      node.match.add_side(node.left.node.match.get_winner())
      node.match.add_side(node.right.node.match.get_winner())

  def generate(self, players):
    number_of_players = len(players)
    
    self.__round = 1
    self.node = None
    self.__set_height(number_of_players)
    self.insert_matches(
      number_of_players, 
      self.__height,
      players)

    self.__create_round()
  
  def advance(self):
    response = ""
    if len(self.__games) != 1:
      self.__round += 1
      self.__promote_winners()
      self.__create_round()

      response = "Tournament bracket advanced to next round."
    else:
      response = "Tournament is over, cannot advance."

    return response

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