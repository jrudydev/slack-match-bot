#!/usr/bin/python

from player import Player


class Tourny:
  def __init__(self):
    self.__players = {}
    self.__games = []

  def get_game_indexes(self):
    number_of_players = len(self.__players)
    size = 2
    while size < number_of_players:
      size *= 2
    half_size = size / 2
    bottom_size = number_of_players / 2
    top_size = bottom_size + number_of_players % 2
    print (top_size, half_size - top_size, bottom_size, half_size - bottom_size)  
  
  def add_player(self, player):
    self.__players[player.get_handle()] = player
       
  def start_tourny():
    t1, t2, b1, b2 = self.get_game_indexes
    for x in range(t1):
      #side_1 = Player("abc", "fname", "lname")
      #side_2 = Player("zyx", "fname", "lname")
      #match = Match(side_1, side_2)
      #games.append(match)
      pass
    return 

  def show_players(self):
    for key in self.__players:
      player = self.__players[key]
      print player.get_name()
    return

  def print_number_of_players(self):
    print cnt(self.__players)


def main(): return

if __name__ == '__main__':
  main()
