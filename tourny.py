#!/usr/bin/python

from player import Player

class Tourny:
  def __init__(self):
    self.__players = {}
    self.__games = []
    
  def add_player(self, player):
    self.__players[player.get_handle()] = player
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
