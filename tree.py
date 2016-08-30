#!/usr/bin/python

class TournyNode(object):
  def __init__(self, key):
    self.key = key
    self.left = None
    self.right = None
    self.match = None

  def __str__(self):
    return str(self.key)
 
  def __repr__(self):
    return str(self.key)


class TournyTree(object):
  def __init__(self):
    self.node = None
    self.height = -1

  def generate(self, players):
    tree.set_height(number_of_players)
    tree.insert(number_of_players, self.__height)

  def insert(self, players, count):
    n = TournyNode(players)
    if not self.node:
      self.node = n
      self.node.left = TournyTree()
      self.node.right = TournyTree()
      
      if count > 1:
        half = players / 2
        self.node.right.insert(half, count - 1)

        if players % 2 == 1: half += 1
        self.node.left.insert(half, count - 1)

  def set_height(self, players):
    self.__height = 1
    bracket_size = 2
    while bracket_size < players:
      bracket_size *= 2
      self.__height += 1

    return self.height
  
  def inorder_traverse(self):
    result = []

    if not self.node:
      return result

    result.extend(self.node.left.inorder_traverse())
    if self.node.left.node == None or self.node.right.node == None:
      result.append(self.node.key)
    result.extend(self.node.right.inorder_traverse())

    return result

if __name__ == '__main__':
  tree = TournyTree()

  number_of_players = 10
  tree.generate(number_of_players)

  print tree.inorder_traverse()
