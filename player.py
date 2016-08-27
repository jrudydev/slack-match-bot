#!/usr/bin/python

from __future__ import print_function

FNAME_INDEX = 0
LNAME_INDEX = 1

WIN_INDEX = 0
LOSS_INDEX = 1

class Player():

  def __init__(self, handle, fname, lname):
    self.__handle = handle
    self.__name_tuple = (fname, lname)
    self.__record_tuple = (0, 0)
    self.__match_id = None

  def set_match_id(self, id):
    self.__match_id = id

  def get_handle(self):
    return self.__handle

  def get_match_id(self):
    return self.__get_match_id 

  def get_name(self):
    return self.__name_tuple[FNAME_INDEX] + ' ' +  self.__name_tuple[LNAME_INDEX]

  def get_record(self):
    wins = self.__record_tuple[WIN_INDEX]
    losses = self.__record_tuple[LOSS_INDEX]
    return "( " + str(wins) + "W - " + str(losses) + "L )"   

  def add_win(self):
    self.__record_touple[WIN_INDEX] += 1

  def add_loss(self):
    self.__record_touple[LOSS_INDEX] += 1 

  def print_name(self):
    print(self.get_name(), end="")

  def print_record(self):
    print(self.get_record())

  def print_name_and_record(self):
    print(self.get_name() + " " + self.get_record())

  def print_win_percent(self):
    wins = self.__record_tuple[WIN_INDEX]
    losses = self.__record_tuple[LOSS_INDEX]
    if wins == 0 and losses == 0:
      print(self.get_name(), "has not played any games.")
      return 0

    if wins == 0:
      print(self.get_name(), "win percent: 0%")
      return 0

    total = self.__record_tuple[WIN_INDEX] + self.__record_tuple[LOSS_INDEX]; 
    print(self.get_name(), "win percent: " + (total / wins) + "%")
 

def main():
  first_player = Player("abcxyz", "Pepe", "Rodo")
  first_player.print_name_and_record()
  first_player.print_win_percent()

if __name__ == '__main__':
  main()
