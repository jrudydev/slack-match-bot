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
    self.__losses_tupe = (0, 0)
    self.__reset_triggers_tuple = (0,0)
    #self.__match_id = 

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
    frist_side_wins = self.__wins_tuple[SIDE_1_INDEX]
    second_side_wins = self.__wins_tuple[SIDE_2_INDEX]

    if frist_side_wins + second_side_wins > BEST_OF:
      print("This game is complete.")
      return

    if self.__match_status() == MATCH_STATUS_NOT_FULL:
      print("Cannot win a bye game.")
      return
    
    first_side = self.__sides_tuple[SIDE_1_INDEX]
    second_side = self.__sides_tuple[SIDE_2_INDEX]

    name = ""
    if first_side.get_user() == user:
      self.__wins_tuple = (frist_side_wins + 1, second_side_wins)
      name = first_side.get_name()

    if second_side.get_user() == user:
      self.__wins_tuple = (frist_side_wins, second_side_wins + 1) 
      name = second_side.get_name()
    
    print name + " gains a point."

  def add_loss(self, user):
    side_1_losses = self.__losses_tuple[SIDE_1_INDEX]
    side_2_losses = self.__losses_tuple[SIDE_2_INDEX]

    if side_1_losses + side_2_losses > BEST_OF:
      print("This game is complete.")
      return
    
    if self.__match_status() == MATCH_STATUS_NOT_FULL:
      print("Cannot loss a bye game.")
      return

    side_1 = self.__sides_tuple[SIDE_1_INDEX]
    side_2 = self.__sides_tuple[SIDE_2_INDEX]

    if side_1.get_handle() == user:
      self.__losses_tuple = (side_1_losses + 1, side_2_losses) 

    if side_2.get_handle() == user:
      self.__losses_tuple = (side_1_losses, side_2_losses + 1) 

  def __match_status(self):
    side_1_points = self.__wins_tuple[SIDE_1_INDEX]
    side_2_points = self.__wins_tuple[SODE_2_INDEX]
 
    if frist_side == None or second_side == None:
      return MATCH_STATUS_NOT_FULL
    if side_1_points == 0 and side_2_points == 0:
      return MATCH_STATUS_NOT_STARTED
    if side_1_points + side_2_points > BEST_OF:
      return MATCH_STATUS_COMPLETE
    else:
      return MATCH_STATUS_IN_PROGRESS

  def request_reset(handle): return

  def get_top(self):
    side = self.__sides_tuple[SIDE_1_INDEX]
    if side == None:
      print "This is a bye game."
      return

    points = self.__wins_tuple[SIDE_1_INDEX]
    return side.get_name() + ": " + str(points)

  def get_bottom(self):
    side = self.__sides_tuple[SIDE_2_INDEX]
    if side == None:
      if self.__sides_tuple[SIDE_1_INDEX] == None:
        print "This is a bye game."
      else:
        print "This side is a bye."
      return
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

  match.add_win(top_player.get_handle())

  match.print_score()


if __name__ == '__main__':
  main()
