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

    if number_of_games == 1:
      return 1, 0, 0, 0

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
    self.__players[player.get_user()] = player
       
  def start_tourny(self):
    size = len(self.__players)
    if size < 2:
      print "There are not enough players."
      return

    for key in self.__players:
      self.__unassigned_players.append(self.__players[key])

    top_games, bye_games_top, bottom_games,  bye_games_bottom = self.__get_bye_games()
    for x in range(top_games):
      first_player = self.__pop_random_unassigned_player()
      if first_player != None:
        first_player.set_match_id(x)
      second_player = self.__pop_random_unassigned_player()
      if second_player != None:
        second_player.set_match_id(x)

      match = Match()
      match.add_side(first_player)
      match.add_side(second_player)
      self.__games.append(match)
   
    for x in range(bye_games_top):
      match = Match()
      self.__games.append(match)

    for x in range(bottom_games):
      first_player = self.__pop_random_unassigned_player()
      if first_player != None:
        first_player.set_match_id(x + top_games + bye_games_top)
      second_player = self.__pop_random_unassigned_player()
      if second_player != None:
        second_player.set_match_id(x + bottom_games + bye_games_bottom)

      match = Match()
      match.add_side(first_player)
      match.add_side(second_player)
      self.__games.append(match)

    for x in range(bye_games_bottom):
      match = Match()
      self.__games.append(match)

  def report_win(self, user):
    if user not in self.__players:
      print "Player not found."
      return

    player = self.__players[user]
    game_id = player.get_match_id()
    match = self.__games[game_id]
    print player.get_name() + " repoted a win."
    match.add_win(user)

  def print_tourny(self):
    for match in self.__games:
      print "Match:"
      match.print_score()
      print ""

  def show_players(self):
    for key in self.__players:
      player = self.__players[key]
      print player.get_name()
    return


def main():
  tourny = Tourny()
  tourny.add_player(Player("U123", "abc", "fabc", "labc"))
  tourny.add_player(Player("U456", "def", "fdef", "ldef"))

  tourny.start_tourny()
  print ""
  
  tourny.print_tourny()
  print ""

  tourny.report_win("U123")
  print ""

  tourny.print_tourny()

if __name__ == '__main__':
  main()
