#!/usr/bin/python

from player import Player

SIDE_1_INDEX = 0
SIDE_2_INDEX = 1 

BEST_OF = 3

MATCH_STATUS_NOT_FULL = 0
MATCH_STATUS_NOT_STARTED = 1
MATCH_STATUS_IN_PROGRESS = 2
MATCH_STATUS_COMPLETE = 3

 
class Match():
  def __init__(self):
    self.__sides_tuple = (None, None)
    self.__wins_tuple = (0, 0)
    self.__reset_triggers_tuple = (0,0)

  def add_side(self, side):
    if self.__sides_tuple[0] == None:
      self.__sides_tuple = (side, None)
      print "Player added added."
    elif self.__sides_tuple[1] == None:
      self.__sides_tuple = (self.__sides_tuple[SIDE_1_INDEX], side)
      print "Player added added."
    else:
      print "This game is full!"

  def add_win(self, user):
    if self.match_status() == MATCH_STATUS_COMPLETE:
      print("This game is complete.")
      return

    if self.match_status() == MATCH_STATUS_NOT_FULL:
      print("Cannot win a bye game.")
      return
    
    first_side = self.__sides_tuple[SIDE_1_INDEX]
    second_side = self.__sides_tuple[SIDE_2_INDEX]
    first_side_wins = self.__wins_tuple[SIDE_1_INDEX]
    second_side_wins = self.__wins_tuple[SIDE_2_INDEX]

    name = ""
    if first_side.get_user() == user:
      self.__wins_tuple = (first_side_wins + 1, second_side_wins)
      name = first_side.get_name()

    if second_side.get_user() == user:
      self.__wins_tuple = (first_side_wins, second_side_wins + 1) 
      name = second_side.get_name()
    
    print name + " gains a point."

  def set_match_ids(self, match_id):
    top_side = self.__sides_tuple[SIDE_1_INDEX]
    bottom_side = self.__sides_tuple[SIDE_2_INDEX]
    if top_side != None:
      top_side.set_match_id(match_id)
    if bottom_side != None:
      bottom_side.set_match_id(match_id)

  def match_status(self):
    first_side = self.__sides_tuple[SIDE_1_INDEX]
    second_side = self.__sides_tuple[SIDE_2_INDEX]
    side_1_points = self.__wins_tuple[SIDE_1_INDEX]
    side_2_points = self.__wins_tuple[SIDE_2_INDEX]

    games_to_win = BEST_OF - 1
    if first_side == None or second_side == None:
      return MATCH_STATUS_NOT_FULL
    if side_1_points == 0 and side_2_points == 0:
      return MATCH_STATUS_NOT_STARTED
    if side_1_points >= games_to_win or side_2_points >= games_to_win:
      return MATCH_STATUS_COMPLETE
    else:
      return MATCH_STATUS_IN_PROGRESS

  def is_complete(self):
    return self.match_status() == MATCH_STATUS_COMPLETE

  def request_reset(handle): return

  def get_top(self):
    output = ""
    side = self.__sides_tuple[SIDE_1_INDEX]
    if side == None:
      output = "This is a bye game."
      return output

    points = self.__wins_tuple[SIDE_1_INDEX]
    return side.get_name() + ": " + str(points)

  def get_bottom(self):
    output = ""
    side = self.__sides_tuple[SIDE_2_INDEX]
    if side == None:
      if self.__sides_tuple[SIDE_1_INDEX] == None:
        output = "This is a bye game."
      else:
        output = "This side is a bye."
      return output
    points = self.__wins_tuple[SIDE_2_INDEX]
    return side.get_name() + ": " + str(points)

  def get_score(self):
    return "%s\n%s" % (self.get_top(), self.get_bottom())
  
  def print_score(self):
    print self.get_score()


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

  match.print_score()


if __name__ == '__main__':
  main()
