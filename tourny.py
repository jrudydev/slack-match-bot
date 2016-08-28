#!/usr/bin/python

from player import Player
from match import Match
import random

class Tourny:
  def __init__(self):
    self.__players = {}
    self.__games = []
    self.__unassigned_players_top = []
    self.__unassigned_players_bottom = []

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

  def __pop_random_unassigned_player_top(self):
    number_of_players = len(self.__unassigned_players_top)
    if number_of_players == 0:
      return None

    rand_int = random.choice(range(number_of_players))
    random_player = self.__unassigned_players_top[rand_int]
    del self.__unassigned_players_top[rand_int]
    return random_player

  def __pop_random_unassigned_player_bottom(self):
    number_of_players = len(self.__unassigned_players_bottom)
    if number_of_players == 0:
      return None

    rand_int = random.choice(range(number_of_players))
    random_player = self.__unassigned_players_bottom[rand_int]
    del self.__unassigned_players_bottom[rand_int]
    return random_player
  
  def add_player(self, player):
    self.__players[player.get_user()] = player
       
  def start_tourny(self):
    size = len(self.__players)
    if size < 2:
      print "There are not enough players."
      return
 
    half_size = size / 2
    i = 0
    for key in self.__players:
      if i < len(self.__players) - half_size:
        self.__unassigned_players_top.append(self.__players[key])
      else:
        self.__unassigned_players_bottom.append(self.__players[key])
      i += 1

    top_games, bye_games_top, bottom_games,  bye_games_bottom = self.__get_bye_games()
    for x in range(top_games):
      first_player = self.__pop_random_unassigned_player_top()
      if first_player != None:
        first_player.set_match_id(x)
      second_player = self.__pop_random_unassigned_player_top()
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
      first_player = self.__pop_random_unassigned_player_bottom()
      if first_player != None:
        first_player.set_match_id(x + top_games + bye_games_top)
      second_player = self.__pop_random_unassigned_player_bottom()
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
    if len(self.__games) == 0:
      print "The tournament has not started."
      return

    if user not in self.__players:
      print "Player not found."
      return

    player = self.__players[user]
    game_id = player.get_match_id()
    match = self.__games[game_id]
    print player.get_name() + " repoted a win."
    match.add_win(user)

  def report_loss(self, user):
    if len(self.__games) == 0:
      print "The tournament has not started."
      return
      
    if user not in self.__players:
      print "Player not found."
      return

    player = self.__players[user]
    game_id = player.get_match_id()
    match = self.__games[game_id]
    print player.get_name() + " repoted a loss."
    match.add_loss(user)

  def get_printed_tourny(self):
    if len(self.__games) == 0:
      print "The tournament has not started."
      return

    string = ""
    i = 1
    for match in self.__games:
      string = "%s\nMatch: %d\n" % (string, i)
      string = "%s%s\n" % (string, match.get_score())
      i += 1
    
    return string

  def print_tourny(self):
    print self.get_printed_tourny()

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
