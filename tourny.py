#!/usr/bin/python

from player import Player
from match import Match
from tree import TournyTree
from match import MATCH_STATUS_COMPLETE
import random

class Tourny:
  def __init__(self):
    self.__players = {}
    self.__bracket = TournyTree()
  
  def add(self, player):
    self.__players[player.get_user()] = player

  def help(self, key):
    # call the readmedocs app
    pass
       
  def start(self):
    number_of_players = len(self.__players)
    if number_of_players < 2:
      print "There are not enough players."
      return
    
    players = []
    for key in self.__players:
      players.append(self.__players[key])
    self.__bracket.generate(players)

  def win(self, user):
    games = self.__bracket.get_games()
    if len(games) == 0:
      return "The tournament has not started."

    if user not in self.__players:
      return "Player not found."
    
    player = self.__players[user]
    game_id = player.get_match_id()
    match = games[game_id]
    match.add_win(user)

    response = ""
    if match.match_status() == MATCH_STATUS_COMPLETE:
      response = player.get_name() + " wins the match."
    else:
      response = player.get_name() + " repoted a win"

    if len(games) == 1 and self.is_complete():
      response += " and is the champion!"
    else:
      response += "."

    return response

  def next(sef):
    if self.is_complete():
      print "Advance to the next round"




  def get_printed(self):
    games = self.__bracket.get_round(1)

    string = ""
    if len(games) == 0:
      return "The tournament has not started."

    i = 1
    for match in games:
      string = "%s\nMatch: %d\n" % (string, i)
      string = "%s%s\n" % (string, match.get_score())
      i += 1
    
    return string

  def print_tourny(self):
    print self.get_printed()

  def is_complete(self):
    games = self.__bracket.get_games()
    for match in games:
      if match.is_complete() == False:
        return False
    
    return True


def main():
  tourny = Tourny()
  tourny.add(Player("U123", "abc", "fabc", "labc"))
  tourny.add(Player("U456", "def", "fdef", "ldef"))

  tourny.start()
  print ""
  
  tourny.print_tourny()
  print ""

  tourny.win("U123")
  print ""

  tourny.print_tourny()

if __name__ == '__main__':
  main()
