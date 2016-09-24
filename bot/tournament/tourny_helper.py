#!/usr/bin/python

# Created by: JRG
# Date: Sept 5, 2016
#
# Description: This object is needed to handle multiple slack channels. An instance of the
# tourny object is hashed with the channel id as the key. This current tourny
# should be passed the channel id at the start of every command.

from tourny import Tourny
from player import Player

USER_INDEX = 0
COMMAND_INDEX = 1


class TournyHelper():
  '''
  This class keeps track of the current channel and handles that object
  in the hash table.
  '''

  __tourny_channels = {}
  __current_channel = None
  __current_command = (None, None, None)

  def set_current_tourny(self, channel):
    tourny = None
    if channel not in self.__tourny_channels:
      self.__tourny_channels[channel] = Tourny()
      
    self.__current_channel = channel

    return tourny

  def set_current_command(self, user, command, channel):
    self.__current_command = (user, command)
    self.set_current_tourny(channel)

  def get_current_user(self):
    return self.__current_command[USER_INDEX]

  def get_current_command(self):
    return self.__current_command[COMMAND_INDEX]

  def get_current_channel(self):
    return self.__current_channel

  def get_current_tourny(self):
    tourny = None
    if self.__current_channel != None:
      tourny = self.__tourny_channels[self.__current_channel]

    return tourny

  def start_singles(self, presets):
    tourny = self.get_current_tourny()
    return tourny.singles(presets)

  def start_doubles(self, presets):
    tourny = self.get_current_tourny()
    return tourny.doubles(self.get_current_user(), presets)

  def next_round(self):
    tourny = self.get_current_tourny()
    return tourny.next()

  def reset_match(self, member_handle):
    tourny = self.get_current_tourny()
    return tourny.reset(member_handle)

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

  def clear_players(self):
    tourny = self.get_current_tourny()
    return tourny.clear()

  def clear_games(self):
    tourny = self.get_current_tourny()
    return tourny.destroy()

  def report_win(self, user_id):
    tourny = self.get_current_tourny()
    return tourny.win(user_id)

  def report_win_with_handle(self, user_handle):
    response = ''
    tourny = self.get_current_tourny()
    user_id = tourny.get_user_id(user_handle)

    return tourny.win(user_id)

  def report_loss(self, user_id):
    tourny = self.get_current_tourny()
    return tourny.loss(user_id)

  def report_loss_with_handle(self, user_handle):
    response = ''
    tourny = self.get_current_tourny()
    user_id = tourny.get_user_id(user_handle)

    return tourny.loss(user_id)

  def is_tourny_in_progress(self):
    tourny = self.get_current_tourny()
    return tourny.is_in_progress()

  def get_tourny(self):
    tourny = self.get_current_tourny()
    return tourny.get_printed()

def main():
  pass

if __name__ == '__main__': 
  main()
