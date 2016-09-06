#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The match object holds a two side tuple and their current
# match score tuple respectively. It track the best of three matches and
# presents the winner.

from player import Player

SIDE_1_INDEX = 0
SIDE_2_INDEX = 1 

BEST_OF = 1

MATCH_STATUS_NOT_FULL = 0
MATCH_STATUS_NOT_STARTED = 1
MATCH_STATUS_IN_PROGRESS = 2
MATCH_STATUS_COMPLETE = 3

 
class Match():
  '''
  This class allows you to add two objects and stores them in a tuple. The score
  is also stored in a tuple respectively.
  '''

  def __init__(self):
    self.__sides_tuple = (None, None)
    self.__wins_tuple = (0, 0)

  def add_side(self, side):
    '''
    Try to add a side to the top and the to the bottom slot  if there is room.
    '''
    response = ""
    if self.__sides_tuple[0] == None:
      self.__sides_tuple = (side, None)
      response = "Player added added to top."
    elif self.__sides_tuple[1] == None:
      self.__sides_tuple = (self.__sides_tuple[SIDE_1_INDEX], side)
      response = "Player added added to bottom."
    else:
      response = "This game is full!"

    print response

  def add_win(self, user):
    '''
    Register a win for the player with the slack user id provided.
    '''
    response = ""
    if self.match_status() == MATCH_STATUS_COMPLETE:
      return "This game is complete."

    if self.match_status() == MATCH_STATUS_NOT_FULL:
      return "Cannot win a bye game."

    top, bottom, top_points, bottom_points = self.__get_tuple()
    if top.get_user() == user:
      self.__wins_tuple = (top_points + 1, bottom_points)
      response = top.get_name()

    if bottom.get_user() == user:
      self.__wins_tuple = (top_points, bottom_points + 1) 
      response = bottom.get_name()

    if response == "":
      response = "Player not found in match."
    else:
      response += " gains a point."
    
    print response

  def quit_player(self, user):
    '''
    This method will disqualify a player with the slack user id provide and
    consiquently give the win to the oppenent.
    '''
    if self.match_status() == MATCH_STATUS_NOT_FULL:
      print("Cannot win a bye game.")
      return
    
    first_side = self.__sides_tuple[SIDE_1_INDEX]
    second_side = self.__sides_tuple[SIDE_2_INDEX]

    response = ""
    if first_side.get_user() == user:
      self.__wins_tuple = (0, BEST_OF - 1)
      response = first_side.get_name()

    if second_side.get_user() == user:
      self.__wins_tuple = (BEST_OF - 1, 0) 
      response = second_side.get_name()

    if response == "":
      response = "Player not found in match."
    else:
      response += " has been disqualified."
    
    print response 

  def set_match_ids(self, match_id):
    '''
    Sets the match ids for the players in the game to later grab them from a list.
    '''
    top = self.__sides_tuple[SIDE_1_INDEX]
    bottom = self.__sides_tuple[SIDE_2_INDEX]
    if top != None:
      top.match_id = match_id
    if bottom != None:
      bottom.match_id = match_id

  def match_status(self):
    top, bottom, top_points, bottom_points = self.__get_tuple()

    response = None
    games_to_win = BEST_OF - 1
    if top == None or bottom == None:
      response = MATCH_STATUS_NOT_FULL
    elif top_points == 0 and bottom_points == 0:
      response = MATCH_STATUS_NOT_STARTED
    elif top_points >= games_to_win or bottom_points >= games_to_win:
      response = MATCH_STATUS_COMPLETE
    else:
      response = MATCH_STATUS_IN_PROGRESS

    return response

  def is_complete(self):
    status = self.match_status()
    return status == MATCH_STATUS_COMPLETE or status == MATCH_STATUS_NOT_FULL

  def get_sides(self):
    return self.__sides_tuple[SIDE_1_INDEX], self.__sides_tuple[SIDE_2_INDEX] 

  def __get_tuple(self):
    return self.__sides_tuple[SIDE_1_INDEX], self.__sides_tuple[SIDE_2_INDEX], \
      self.__wins_tuple[SIDE_1_INDEX], self.__wins_tuple[SIDE_2_INDEX]

  def get_winner(self):
    '''
    Return the side with has won the majority of the games and handle bye match
    '''
    response = None
    if not self.is_complete():
      print "This game has not been completed."
    else:
      top, bottom, top_points, bottom_points = self.__get_tuple()

      if bottom == None:
        response = top
      if top_points == BEST_OF:
        response = top
      if bottom_points == BEST_OF:
        response = bottom 

    return response 

  def get_top(self):
    '''
    Display the top side along with the score.
    '''
    output = ""
    side = self.__sides_tuple[SIDE_1_INDEX]
    if side == None:
      output = "This is a bye game."
    else:
      points = self.__wins_tuple[SIDE_1_INDEX]
      output = side.get_name() + ": " + str(points)

    return output

  def get_bottom(self):
    '''
    Display the bottom side along with the score.
    '''
    output = ""
    side = self.__sides_tuple[SIDE_2_INDEX]
    if side == None:
      if self.__sides_tuple[SIDE_1_INDEX] == None:
        output = "This is a bye game."
      else:
        output = "This side is a bye."
    else:
      points = self.__wins_tuple[SIDE_2_INDEX]
      output = side.get_name() + ": " + str(points)

    return output

  def get_score(self):
    return "%s\n%s" % (self.get_top(), self.get_bottom())


def main(): 
  top_player = Player("U234135", "abc", "Pepe", "Rodo") 
  bottom_player = Player("U234355", "ZXY", "Papi", "Chulo") 

  match = Match()
  print match.get_bottom()
  match.print_score()
  print ""

  match.add_side(top_player)
  print match.get_top()
  print match.get_bottom()
  print ""

  match.add_side(bottom_player)
  print match.get_top()
  print match.get_bottom()
  print ""

  match.add_win(top_player.get_user())

  print match.get_score()


if __name__ == '__main__':
  main()
