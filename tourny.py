#!/usr/bin/python

from player import Player
from match import Match
import random

class Tourny:
  def __init__(self):
    self.__players = {}
    self.__games = []
    self.__unassigned_players = []

  def __get_bye_games(self):
    number_of_players = len(self.__players)
    number_of_games = number_of_players / 2
    if number_of_players % 2 == 1:
      number_of_games += 1

    size = 2
    while size < number_of_games:
      size *= 2
    half_size = size / 2

    bottom_size = number_of_games / 2
    top_size = bottom_size + number_of_games % 2
    return top_size, half_size - top_size, bottom_size, half_size - bottom_size

  def __pop_random_unassigned_player(self):
    number_of_players = len(self.__unassigned_players)
    if number_of_players == 0:
      return None

    rand_int = random.choice(range(number_of_players))
    random_player = self.__unassigned_players[rand_int]
    del self.__unassigned_players[rand_int]
    return random_player
  
  def add_player(self, player):
    self.__players[player.get_handle()] = player
       
  def start_tourny(self):
    size = len(self.__players)
    if size < 2:
      print "There are not enough players."
      return

    for key in self.__players:
      self.__unassigned_players.append(self.__players[key])

    top_games, bye_games_top, bottom_games,  bye_games_bottom = self.__get_bye_games()
    for x in range(top_games):
      match = Match()
      match.add_side(self.__pop_random_unassigned_player())
      match.add_side(self.__pop_random_unassigned_player())
      self.__games.append(match)
   
    for x in range(bye_games_top):
      match = Match()
      self.__games.append(match)

    for x in range(bottom_games):
      match = Match()
      match.add_side(self.__pop_random_unassigned_player())
      match.add_side(self.__pop_random_unassigned_player())
      self.__games.append(match)

    for x in range(bye_games_bottom):
      match = Match()
      self.__games.append(match)

  def print_tourny(self):
    for match in self.__games:
      print "Match:"
      match.print_score()

  def show_players(self):
    for key in self.__players:
      player = self.__players[key]
      print player.get_name()
    return


def main():
  tourny = Tourny()
  tourny.add_player(Player("abc", "fabc", "labc"))
  tourny.add_player(Player("def", "fdef", "ldef"))
  tourny.start_tourny()
  tourny.print_tourny()

if __name__ == '__main__':
  main()
