#!/usr/bin/python

# Created by: JRG
# Date: Sept 5, 2016
#
# Description: This allows the creating of a doubles tournament bracket. It contains
# two or more players objects and also handles setting their match ids.

from player import Player

FNAME_INDEX = 0
LNAME_INDEX = 1

WIN_INDEX = 0
LOSS_INDEX = 1

class PendingTeam():
  '''
  This is a place holder object for pending matches.
  '''
  def __init__(self, pending_match):
    self.__pending_match = pending_match

  def get_pending_match(self):
    return self.__pending_match


class PlayerTeam():
  '''
  The team object can have as many players as needed.
  '''

  def __init__(self):
    self.__players = []

  def add_player(self, player):
    self.__players.append(player)

  def set_match_id(self, match_id):
    for player in self.__players:
      player.set_match_id(match_id)

  def get_match_id(self):
    first_player = self.__players[0]
    return first_player.get_match_id()

  def get_users(self):
    users = []
    for player in self.__players:
      users.append(player.get_user())
    return users

  def get_player_names(self):
    '''
    Returns the handles and names separated by ampersand(&)
    '''
    handles = []
    for player in self.__players:
      handles.append(player.get_handle_and_name())
    return " & ".join(handles)

  def is_single_player(self):
    return len(self.__players) == 1

  def is_empty(self):
    return len(self.__players) == 0


def main():
  first_team = Team(["U2343255", "U2343256"], ["abcxyz", "ABCXYXZ"], ["Pepe", "Rodo"])
  print first_team.get_name()

if __name__ == '__main__':
  main()
