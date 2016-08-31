#!/usr/bin/python

from player import Player
from match import Match
from match import MATCH_STATUS_COMPLETE
import random

class Tourny:
  def __init__(self):
    self.__players = {}
    self.__unassigned_players = []
    self.__tree = None
    self.__games = None
    self.__round = -1    

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
    number_of_players = len(self.__players)
    if number_of_players < 2:
      print "There are not enough players."
      return
    
    for key in self.__players:
      self.__unassigned_players.append(self.__players[key])
    
    tree = TournyTree(len(self.__unassigned_players))
    '''
    self.__games = []
    for x in range(half_of_the_bracket):
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

    for x in range(half_of_the_bracket):
      first_player = self.__pop_random_unassigned_player_bottom()
      if first_player != None:
        first_player.set_match_id(x + half_of_the_bracket)
      second_player = self.__pop_random_unassigned_player_bottom()
      if second_player != None:
        second_player.set_match_id(x + half_of_the_bracket)

      match = Match()
      match.add_side(first_player)
      match.add_side(second_player)
      self.__games.append(match)

    self.print_tourny()
    '''
  def report_win(self, user):
    if len(self.__games) == 0:
      return "The tournament has not started."

    if user not in self.__players:
      return "Player not found."
    
    player = self.__players[user]
    game_id = player.get_match_id()
    match = self.__games[game_id]
    match.add_win(user)

    response = ""
    if match.match_status() == MATCH_STATUS_COMPLETE:
      response = player.get_name() + " wins the match."
    else:
      response = player.get_name() + " repoted a win"

    if len(self.__games) == 1 and self.is_complete():
      response += " and is the champion!"
    else:
      response += "."

    return response

  def next_rount(sef):
    if self.is_complete():
      print "Advance to the next round"

  def get_printed_tourny(self):
    string = ""
    if len(self.__games) == 0:
      output = "The tournament has not started."
      print output
      return output

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

  def get_size(self):
    return len(self.__players)

  def is_complete(self):
    for match in self.__games:
      if match.is_complete() == False:
        return False
    
    return True


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
