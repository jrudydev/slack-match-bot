#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The tree object replicates a trounmanet bracket. The height
# is set depeding on the number of players. The size will double to 
# accommodate any number of players with an even distribution.

from match import Match
from player import Player
from team import PlayerTeam
import random

class TourneyNode(object):
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


class TourneyTree(object):
  '''
  The tree is initializes with a list of players and generates all the
  games of the tournament with the root node containing the championship game.
  '''

  def __init__(self):
    self.node = None
    self.__matches = []
    self.__round = -1
    self.__height = -1

  def insert_matches(self, key, count, slots, is_random):
    '''
    Generates the tree of empty matches starting at the root node and
    adding slots at the leaves.
    '''
    n = TourneyNode(key)
    if not self.node:
      self.node = n
      self.node.left = TourneyTree()
      self.node.right = TourneyTree()
      self.node.match = Match()
      
      if count > 1:
        # non leaf nodes have an empty match object inserted to them
        half = key / 2
        self.node.right.insert_matches(half, count - 1, slots, is_random)

        if key % 2 == 1: half += 1
        self.node.left.insert_matches(half, count - 1, slots, is_random)
      else:
        # leaf node reached so add one or two slots to the game
        for x in range(self.node.key):
          if is_random:
            # pop a random slot
            number_of_slots = len(slots)
            index = random.choice(range(number_of_slots))
            random_slot = slots[index]
          else:
            index = 0
            random_slot = slots[index]
          
          del slots[index]

          self.node.match.add_slot(random_slot)

  def generate(self, slots, random):
    '''
    Initalize and reset the tree with the slots provided.
    '''
    self.destroy()

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
    if len(self.__matches) != 1:
      self.__round += 1
      self.__promote_winners()
      self.__create_round()

      response = "Tournament bracket advanced to next round."
    else:
      response = "Tournament is over."

    return response

  def get_round_matches(self):
    return self.__matches

  def destroy(self):
    del self.__matches[:]
    self.__round = -1
    self.__height = -1

    nodes = self.__traverse_all_nodes()
    del nodes[:]

  def __set_height(self, slots):
    '''
    Caculate the height of the tree based on the number of players
    '''
    height = 1
    bracket_size = 2
    while bracket_size < slots:
      bracket_size *= 2
      height += 1

    self.__height = height

  def __traverse_all_nodes(self):
    '''
    Traverse tree in order and return the rows.
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
    Assign the match ids to the slots before every round.
    '''
    self.__matches = self.__load_round_matches()
    for x in range(len(self.__matches)):
      self.__matches[x].set_match_ids(x)

  def __promote_winners(self):
    '''
    Draw the winners from the previous round to populate the current one.
    '''
    for node in self.__load_round_nodes():
      node.match.add_slot(node.left.node.match.get_winner())
      node.match.add_slot(node.right.node.match.get_winner())
  

if __name__ == '__main__':
  tree = TourneyTree()

  player_1 = Player("1U555", "jru", "ru", "go")
  slot_1 = PlayerTeam()
  slot_1.add_player(player_1)

  player_2 = Player("2U123", "abc", "fabc", "labc")
  slot_2 = PlayerTeam()
  slot_2.add_player(player_2)

  player_3 = Player("3U456", "def", "fdef", "ldef")
  slot_3 = PlayerTeam()
  slot_3.add_player(player_3)

  player_4 = Player("4U789", "efg", "fefg", "lefg")
  slot_4 = PlayerTeam()
  slot_4.add_player(player_4)

  slots = [
    slot_1,
    slot_2, 
    slot_3, 
    slot_4]
  tree.generate(slots, False)

  matches = tree.get_round_matches()
  for match in matches:
    print match.get_score()

  matches[slot_2.get_match_id()].add_win("2U123")

  for match in matches:
    print match.get_score()