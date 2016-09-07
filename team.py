#!/usr/bin/python

# Created by: JRG
# Date: Sept 5, 2016
#
# Description: 

from player import Player

FNAME_INDEX = 0
LNAME_INDEX = 1

WIN_INDEX = 0
LOSS_INDEX = 1


class Team():
  '''
  The team object can have as many players as needed.
  '''

  def __init__(self):
    self.__teammates = []
    self.__match_id = None

  def add_teammate(self, teammate):
    self.__teammates.append(teammate)

  def set_match_id(self, match_id):
    self.__match_id = match_id
    self.__teammates[0].set_match_id(match_id)
    self.__teammates[1].set_match_id(match_id)

  def get_match_id(self):
    return self.__match_id

  def get_users(self):
    users = []
    for teammate in self.__teammates:
      users.append(teammate.get_user())
    return users

  def get_handles(self):
    handles = []
    for teammate in self.__teammates:
      handles.append(teammate.get_handle())
    return handles

  def get_name(self):
    '''
    Returns a string with the first names unless it do not exist, 
    then it used the handle which always exists.
    '''
    handles = []
    for teammate in self.__teammates:
      handles.append(teammate.get_handle())
    return " & ".join(handles)


def main():
  first_team = Team(["U2343255", "U2343256"], ["abcxyz", "ABCXYXZ"], ["Pepe", "Rodo"])
  print first_team.get_name()

if __name__ == '__main__':
  main()
