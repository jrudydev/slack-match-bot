#!/usr/bin/python

# Created by: JRG
# Date: Sept 29, 2016
#
# Description: This object is needed to handle multiple slack channels. An instance of the
# tournament object is hashed with the channel id as the key. This current tournament
# should be passed the channel id at the start of every command.

from tourney import Tourney
from player import Player

USER_INDEX = 0
COMMAND_INDEX = 1


class TourneyHelper():
  '''
  This class keeps track of the current channel and handles that object
  in the hash table.
  '''

  __tourney_channels = {}
  __current_channel = None
  __current_command = (None, None, None)

  def set_current_tourney(self, channel):
    tourney = None
    if channel not in self.__tourney_channels:
      self.__tourney_channels[channel] = Tourney()
      
    self.__current_channel = channel

    return tourney

  def set_current_command(self, user, command, channel):
    self.__current_command = (user, command)
    self.set_current_tourney(channel)

  def get_current_user(self):
    return self.__current_command[USER_INDEX]

  def get_current_command(self):
    return self.__current_command[COMMAND_INDEX]

  def get_current_channel(self):
    return self.__current_channel

  def get_current_tourney(self):
    tourney = None
    if self.__current_channel != None:
      tourney = self.__tourney_channels[self.__current_channel]

    return tourney

  def start_singles(self):
    tourney = self.get_current_tourney()
    return tourney.singles()

  def start_doubles(self):
    tourney = self.get_current_tourney()
    return tourney.doubles(self.get_current_user())

  def next_round(self):
    tourney = self.get_current_tourney()
    return tourney.next()

  def reset_match(self, member_handle):
    tourney = self.get_current_tourney()
    return tourney.reset(member_handle)

  def add_user(self, member_info):
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

    tourney = self.get_current_tourney()
    return tourney.add_channel_user(Player(member_info["id"], member_info["name"], first_name, last_name))

  def remove(self, player_id):
    tourney = self.get_current_tourney()
    return tourney.remove_player(player_id)

  def clear_current(self):
    tourney = self.get_current_tourney()
    return tourney.clear_users()

  def clear_games(self, tourney):
    return tourney.destroy()

  def report_win(self, user_id):
    tourney = self.get_current_tourney()
    return tourney.win(user_id)

  def report_win_with_handle(self, user_handle):
    response = ''
    tourney = self.get_current_tourney()
    user_id = tourney.get_user_id(user_handle)

    return tourney.win(user_id)

  def report_loss(self, user_id):
    tourney = self.get_current_tourney()
    return tourney.loss(user_id)

  def report_loss_with_handle(self, user_handle):
    response = ''
    tourney = self.get_current_tourney()
    user_id = tourney.get_user_id(user_handle)

    return tourney.loss(user_id)

  def report_join(self, user_id):
    tourney = self.get_current_tourney()
    return tourney.add_participant(user_id)

  def report_boot(self, user_id):
    tourney = self.get_current_tourney()
    return tourney.boot_participant(user_id)

  def is_tourney_in_progress(self):
    tourney = self.get_current_tourney()
    number_of_matches = len(tourney.get_round_matches())
    return not tourney.is_round_complete() or number_of_matches > 1

  def get_tourney(self):
    tourney = self.get_current_tourney()
    return tourney.get_printed()

def main():
  pass

if __name__ == '__main__': 
  main()
