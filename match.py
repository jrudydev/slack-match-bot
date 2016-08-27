#!/usr/bin/python

from player import Player

SIDE_1_INDEX = 0
SIDE_2_INDEX = 1 

BEST_OF = 3

MATCH_STATUS_NOT_STARTED = 0
MATCH_STATUS_IN_PROGRESS = 1
MATCH_STATUS_COMPLETE = 2

 
class Match():
  def __init__(self, side_1, side_2):
    self.__sides_tuple = (side_1, side_2)
    self.__wins_tuple = (0, 0)
    self.__losses_tupe = (0, 0)
    self.__reset_triggers_tuple = (0,0)
    #self.__match_id = 

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

  def print_top(self):
    side = self.__sides_tuple[SIDE_1_INDEX]
    points = self.__wins_tuple[SIDE_1_INDEX]
    print side.get_name() + ": " + str(points)

  def print_bottom(self):
    side = self.__sides_tuple[SIDE_2_INDEX]
    points = self.__wins_tuple[SIDE_2_INDEX]
    print side.get_name() + ": " + str(points)

  def print_score(self):
    self.print_top()
    self.print_bottom()


def main(): 
  top_player = Player("abc", "Pepe", "Rodo") 
  bottom_player = Player("ZXY", "Papi", "Chulo") 

  match = Match(top_player, bottom_player)
  #match.print_top()
  #match.print_bottom()

  match.add_win(top_player.get_handle())

  match.print_score()


if __name__ == '__main__':
  main()
