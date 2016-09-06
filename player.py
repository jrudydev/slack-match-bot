#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The player object will be used for single elimination best 
# of three tournament. It also tracks the wins and losses to display the
# record and/or win percent.

FNAME_INDEX = 0
LNAME_INDEX = 1

WIN_INDEX = 0
LOSS_INDEX = 1


class Player():
  '''
  The player object should be created by passing a unique slack user id, 
  the team user handle, along with a first and last name tuple. The match id 
  instance variable will be set to index the current match.
  '''

  def __init__(self, user,  handle, fname, lname):
    self.__user = user
    self.__handle = handle
    self.__name_tuple = (fname, lname)
    self.__match_id = None

  def get_user(self):
    return self.__user

  def get_handle(self):
    return self.__handle

  def get_name(self):
    return self.__handle

  def set_match_id(self, match_id):
    self.__match_id = match_id

  def get_match_id(self):
    return self.__match_id

  # def get_record(self):
  #   wins = self.__record_tuple[WIN_INDEX]
  #   losses = self.__record_tuple[LOSS_INDEX]
  #   return "( " + str(wins) + "W - " + str(losses) + "L )"   

  # def add_win(self):
  #   self.__record_touple[WIN_INDEX] += 1

  # def add_loss(self):
  #   self.__record_touple[LOSS_INDEX] += 1 

  # def get_win_percent_tuple(self):
  #   '''
  #   Returns the win percent based on the values in the record tuple if the
  #   form of a tuple conatining a percent and response string.
  #   '''
  #   wins = self.__record_tuple[WIN_INDEX]
  #   losses = self.__record_tuple[LOSS_INDEX]
  #   percent = 0
  #   if wins == 0 and losses == 0:
  #     return (percent, self.get_name() + " has not played any games.")

  #   if wins == 0:
  #     return (percent, self.get_name() + " has a win percent of 0%")

  #   total = self.__record_tuple[WIN_INDEX] + self.__record_tuple[LOSS_INDEX]; 
  #   percent = total / wins #TO-DO: This needs to be formatted
  #   return (percent, self.get_name(), "win percent: " + percent + "%")

  # def get_win_percent(self):
  #   response = self.get_win_percent_tuple()
  #   return response[0]

  # def get_win_percent_string(self):
  #   response = self.get_win_percent_tuple()
  #   return response[1]

def main():
  first_player = Player("U2343255", "abcxyz", "Pepe", "Rodo")
  print first_player.get_name() + first_player.get_record()
  print first_player.print_win_percent_string()
  print first_player.get_name() 

if __name__ == '__main__':
  main()
