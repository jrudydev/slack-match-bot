#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The match object holds a two side tuple and their current
# match score tuple respectively. It track the best of three matches and
# presents the winner.

from player import Player
from team import PlayerTeam

TOP_INDEX = 0
BOTTOM_INDEX = 1 

POINTS_TO_WIN = 1

MATCH_STATUS_NOT_FULL = 0
MATCH_STATUS_NOT_STARTED = 1
MATCH_STATUS_IN_PROGRESS = 2
MATCH_STATUS_COMPLETE = 3
MATCH_STATUS_PENDING = 4
 
class Match():
  '''
  This class allows you to add two objects and stores them in a tuple. The score
  is also stored in a tuple respectively.
  '''

  def __init__(self):
    self.__slots_tuple = (None, None)
    self.__wins_tuple = (0, 0)
    # self.__match_number = match_number
    self.__is_pending = False

  def add_slot(self, slot):
    '''
    Try to add a slot to the top and the to the bottom slot  if there is room.
    '''
    response = ""
    if self.__slots_tuple[0] == None:
      self.__slots_tuple = (slot, None)
      #To-Do: check if slot is of type pending and set instance veriable
      response = "Top player added."
      # response = "Top player added to match {}.".format(str(self.__match_number))
    elif self.__slots_tuple[1] == None:
      self.__slots_tuple = (self.__slots_tuple[TOP_INDEX], slot)
      #To-Do: check if slot is of type pending and set instance veriable
      response = "Bottom player added."
      # response = "Bottom player added to match {}.".format(str(self.__match_number))
    else:
      response = "This game is full!"

    print response

  def add_win(self, user):
    '''
    Register a win for the player with the slack user id provided.
    '''
    if self.is_bye_pending():
      return "Cannot reset a bye/pending match."

    if self.is_complete():
      return "Match already won by " + self.get_winner().get_handle_and_name() + "."

    top_slot, bottom_slot, top_points, bottom_points = self.__get_tuples()
    is_top_winner, is_bottom_winner = self.__get_user_slot(top_slot, bottom_slot, user)
 
    response = ""
    if is_top_winner:
      self.__wins_tuple = (top_points + 1, bottom_points)
      response = top_slot.get_handle_and_name()
    if is_bottom_winner:
      self.__wins_tuple = (top_points, bottom_points + 1)
      response = bottom_slot.get_handle_and_name()
    
    is_singles = top_slot.is_single_player()
    if response == "":
      response = "Player not found in match."
    else:
      if is_singles:
        response += " wins!"
      else:
        response += " win!"
    
    print response
    return response

  def add_loss(self, user):
    '''
    Register a loss for the player with the slack user id provided.
    '''
    if self.is_bye_pending():
      return "Cannot reset a bye/pending match."

    if self.is_complete():
      return "Match already been lost by " + self.get_winner().get_handle_and_name() + "."

    top_slot, bottom_slot, top_points, bottom_points = self.__get_tuples()
    is_top_loser, is_bottom_loser = self.__get_user_slot(top_slot, bottom_slot, user)

    response = ""
    if is_top_loser:
      self.__wins_tuple = (top_points, bottom_points + 1)
      response = top_slot.get_handle_and_name()
    if is_bottom_loser:
      self.__wins_tuple = (top_points + 1, bottom_points)
      response = bottom_slot.get_handle_and_name()
    
    is_singles = bottom_slot.is_singles()
    if response == "":
      response = "Player not found in match."
    else:
      if is_singles:
        response += " loses!"
      else:
        response += " lose!"
    
    return response

  def reset_game(self, user):
    '''
    
    '''
    if self.is_bye_pending():
      return "Cannot reset a bye/pending match."
    
    self.__wins_tuple = (0, 0)

    return "Match has been reset."

  def set_match_ids(self, match_id):
    '''
    Sets the match ids for the players in the game to later grab them from a list.
    '''
    top = self.__slots_tuple[TOP_INDEX]
    bottom = self.__slots_tuple[BOTTOM_INDEX]
    if top != None:
      top.set_match_id(match_id)
    if bottom != None:
      bottom.set_match_id(match_id)

  def match_status(self):
    top, bottom, top_points, bottom_points = self.__get_tuples()

    response = None
    if top == None or bottom == None:
      response = MATCH_STATUS_NOT_FULL
    elif self.__is_pending:
      response = MATCH_STATUS_PENDING
    elif top_points == 0 and bottom_points == 0:
      response = MATCH_STATUS_NOT_STARTED
    elif top_points >= POINTS_TO_WIN or bottom_points >= POINTS_TO_WIN:
      response = MATCH_STATUS_COMPLETE
    else:
      response = MATCH_STATUS_IN_PROGRESS

    return response

  def is_bye_pending(self):
    status = self.match_status()
    return status == MATCH_STATUS_NOT_FULL or status == MATCH_STATUS_PENDING

  def is_complete(self):
    status = self.match_status()
    return status == MATCH_STATUS_COMPLETE or status == MATCH_STATUS_NOT_FULL

  def get_sides(self):
    return self.__slots_tuple[TOP_INDEX], self.__slots_tuple[BOTTOM_INDEX]

  def get_score(self):
    return "%s\n%s" % (self.get_top(), self.get_bottom())

  def get_winner(self):
    '''
    Return the slot that has won the match and handle bye match
    '''
    response = None
    if not self.is_complete():
      print "This game has not been completed."
    else:
      top, bottom, top_points, bottom_points = self.__get_tuples()

      if bottom == None:
        response = top
      if top_points == POINTS_TO_WIN:
        response = top
      if bottom_points == POINTS_TO_WIN:
        response = bottom 

    return response

  def get_loser(self):
    '''
    Return the lost the match and handle bye match
    '''
    response = None
    if not self.is_complete():
      print "This game has not been completed."
    else:
      top, bottom, top_points, bottom_points = self.__get_tuples()

      if bottom == None:
        response = bottom
      if top_points == POINTS_TO_WIN:
        response = bottom
      if bottom_points == POINTS_TO_WIN:
        response = top 

    return response 

  def get_top(self):
    '''
    Display the top slot along with the score.
    '''
    output = ""
    slot = self.__slots_tuple[TOP_INDEX]
    if slot == None:
      output = "This is a bye game."
    elif self.__slots_tuple[BOTTOM_INDEX] == None:
      output = "_BYE_:  " + slot.get_handle_and_name()
    else:
      points = self.__wins_tuple[TOP_INDEX]
      output = self.__get_status_label(points) + ":  " + slot.get_handle_and_name()

    return output

  def get_bottom(self):
    '''
    Display the bottom slot along with the score.
    '''
    output = ""
    slot = self.__slots_tuple[BOTTOM_INDEX]
    if slot == None:
      if self.__slots_tuple[TOP_INDEX] == None:
        output = "This is a bye game."
      else:
        output = "_BYE_:  - Bye -"
    else:
      points = self.__wins_tuple[BOTTOM_INDEX]
      output = self.__get_status_label(points) + ":  " + slot.get_handle_and_name()

    return output

  def __get_status_label(self, slot_points):
    label = ""
    status = self.match_status()
    if status == MATCH_STATUS_NOT_STARTED or status == MATCH_STATUS_NOT_FULL:
      label = "_TBD_"
    elif status == MATCH_STATUS_COMPLETE:
      if slot_points == POINTS_TO_WIN:
        label = "_W_".center(5)
      else:
        label = "_L_".center(5)
    else:
      label = str(points).center(10)

    return label

  def __get_user_slot(self, top, bottom, user_id):
    is_top_slot = False
    is_bottom_slot = False
    if user_id in top.get_users():
      is_top_slot = True
    if user_id in bottom.get_users():
      is_bottom_slot = True
    return (is_top_slot, is_bottom_slot)

  def __get_tuples(self):
    return self.__slots_tuple[TOP_INDEX], self.__slots_tuple[BOTTOM_INDEX], \
      self.__wins_tuple[TOP_INDEX], self.__wins_tuple[BOTTOM_INDEX]


def main():
  top_player = Player("U234135", "abc", "Pepe", "Rodo")
  top_slot = PlayerTeam()
  top_slot.add_player(top_player)

  bottom_player = Player("U234355", "ZXY", "Papi", "Chulo")
  bottom_slot = PlayerTeam()
  bottom_slot.add_player(bottom_player)
  
  match = Match()
  print match.get_bottom()
  print match.get_score()
  print ""

  match.add_slot(top_slot)
  print match.get_top()
  print match.get_bottom()
  print ""

  match.add_slot(bottom_slot)
  print match.get_top()
  print match.get_bottom()
  print ""

  match.add_win("U234135")

  print match.get_score()


if __name__ == '__main__':
  main()
