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
      print "Top side added."
    elif self.__sides_tuple[1] == None:
      self.__sides_tuple = (self.__sides_tuple[SIDE_1_INDEX], side)
      print "Bottom side added."
    else:
      print "This game is full!"

  def add_win(self, handle):
    side_1_wins = self.__wins_tuple[SIDE_1_INDEX]
    side_2_wins = self.__wins_tuple[SIDE_2_INDEX]

    if side_1_wins + side_2_wins > BEST_OF:
      print("This game is complete.")
      return
    
    side_1 = self.__sides_tuple[SIDE_1_INDEX]
    side_2 = self.__sides_tuple[SIDE_2_INDEX]

    if side_1.get_handle() == handle:
      self.__wins_tuple = (side_1_wins + 1, side_2_wins) 

    if side_2.get_handle() == handle:
      self.__wins_tuple = (side_1_wins, side_2_wins + 1) 
    
    print handle + " gains a point."

  def add_loss(self, handle):
    side_1_losses = self.__losses_tuple[SIDE_1_INDEX]
    side_2_losses = self.__losses_tuple[SIDE_2_INDEX]

    if side_1_losses + side_2_losses > BEST_OF:
      print("This game is complete.")
      return

    side_1 = self.__sides_tuple[SIDE_1_INDEX]
    side_2 = self.__sides_tuple[SIDE_2_INDEX]

    if side_1.get_handle() == handle:
      self.__losses_tuple = (side_1_losses + 1, side_2_losses) 

    if side_2.get_handle() == handle:
      self.__losses_tuple = (side_1_losses, side_2_losses + 1) 

  def match_status(self):
    side_1_points = self.__wins_tuple[SIDE_1_INDEX]
    side_2_points = self.__wins_tuple[SODE_2_INDEX]
 
    if side_1_points == 0 and side_2_points == 0:
      return MATCH_STATUS_NOT_STARTED
    if side_1_points + side_2_points > BEST_OF:
      return MATCH_STATUS_COMPLETE
    else:
      return MATCH_STATUS_IN_PROGRESS

  def request_reset(handle): return

  def print_test(self):
    side = self.__sides_tuple[SIDE_1_INDEX]
    if side == None:
      print "This is a bye game."
      return
    print side
    points = self.__wins_tuple[SIDE_1_INDEX]
    #print side.get_name() + ": " + str(points)

  def print_top(self):
    side = self.__sides_tuple[SIDE_1_INDEX]
    if side == None:
      print "This is a bye game."
      return

    points = self.__wins_tuple[SIDE_1_INDEX]
    print side.get_name() + ": " + str(points)

  def print_bottom(self):
    side = self.__sides_tuple[SIDE_2_INDEX]
    if side == None:
      if self.__sides_tuple[SIDE_1_INDEX] == None:
        print "This is a bye game."
      else:
        print "This side is a bye."
      return
    points = self.__wins_tuple[SIDE_2_INDEX]
    print side.get_name() + ": " + str(points)

  def print_score(self):
    self.print_top()
    self.print_bottom()


def main(): 
  top_player = Player("abc", "Pepe", "Rodo") 
  bottom_player = Player("ZXY", "Papi", "Chulo") 

  match = Match()
  match.print_bottom()
  match.print_score()
  print ""

  match.add_side(top_player)
  match.print_top()
  match.print_bottom()
  print ""

  match.add_side(bottom_player)
  match.print_top()
  match.print_bottom()
  print ""

  match.add_win(top_player.get_handle())

  match.print_score()


if __name__ == '__main__':
  main()
