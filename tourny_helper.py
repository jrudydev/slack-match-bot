#!/usr/bin/python

# Created by: JRG
# Date: Sept 5, 2016
#
# Description: 

from tourny import Tourny
from player import Player

class TournyHelper():
  __tourny_channels = {}
  __current_channel = None

  def set_current_tourny(self, channel):
    tourny = None
    if channel not in self.__tourny_channels:
      self.__tourny_channels[channel] = Tourny()
      
    self.__current_channel = channel

    return tourny

  def get_current_tourny(self):
    tourny = None
    if self.__current_channel != None:
      tourny = self.__tourny_channels[self.__current_channel]

    return tourny

  def start_tourny(self):
    tourny = self.get_current_tourny()
    return tourny.start()

  def next_round(self, member_handle):
    tourny = self.get_current_tourny()
    return tourny.next()

  def boot_player(self, member_handle):
    tourny = self.get_current_tourny()
    return tourny.boot(member_handle)

  def add_player(self, member_info):
    '''
    Add the user to the tournament
    '''
    if 'profile' in member_info:
      profile = member_info.get('profile')
    first_name = ""
    if "first_name" in profile:
      first_name = profile.get("first_name")
    last_name = ""
    if "last_name" in profile:
      last_name = profile.get("last_name")

    tourny = self.get_current_tourny()
    return tourny.add(Player(member_info["id"], member_info["name"], first_name, last_name))

  def report_win(self, user_handle):
    tourny = self.get_current_tourny()
    return tourny.win(user_handle)

  def get_tourny(self):
    tourny = self.get_current_tourny()
    return tourny.get_printed()

def main():
  pass

if __name__ == '__main__': 
  main()