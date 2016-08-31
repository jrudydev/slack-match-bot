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
    self.__round = 1

  def __get_height(self, players):
    height = 1
    bracket_size = 2
    while bracket_size < players:
      bracket_size *= 2
      height += 1

    return height

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

  def inorder_traverse(self):
    result = []

    if not self.node:
      return result

    result.extend(self.node.left.inorder_traverse())
    if self.node.left.node == None or self.node.right.node == None:
      result.append(self.node.match) 
    result.extend(self.node.right.inorder_traverse())

    return result

  def __set_round(self, round):

    #!!! Need to traverse only to round height

    self.__games = tree.inorder_traverse()
    for x in range(len(self.__games)):
      self.__games[x].set_match_ids(x)

  def generate(self, players):
    number_of_players = len(players)
    
    self.node = None
    tree.insert_matches(
      number_of_players, 
      self.__get_height(number_of_players),
      players)

    self.__set_round(self.__round)
  

if __name__ == '__main__':
  tree = TournyTree()
  first_player = Player("U555", "jru", "ru", "go")

  players = [
    first_player,
    Player("U123", "abc", "fabc", "labc"), 
    Player("U456", "def", "fdef", "ldef"), 
    Player("U789", "efg", "fefg", "lefg")]
  tree.generate(players)

  games = tree.inorder_traverse()
  for match in games:
    print match.get_score()

  print str(first_player.get_match_id())
  print ""

  games[first_player.get_match_id()].add_win("U555")

  games = tree.inorder_traverse()
  for match in games:
    print match.get_score()