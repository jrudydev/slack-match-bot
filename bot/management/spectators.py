#!/usr/bin/python

# Created by: JRG
# Date: Sept 18, 2016
#
# Description: This object manages the spectator users in the channel. You can add
# users, list them, and clear the entire list. There is also a convenience
# method to check if a user is a spectator.

class Spectators():
  '''
  This class contains a list of users that are just spectating
  '''

  def __init__(self):
  	self.__spectators = []

  def clear_users(self):
    del self.__spectators[:]

    return "Removing all spectators."

  def list_users(self):
    response = "Spectators:\n"
    if len(self.__spectators) == 0:
      response += "None"
    
    i = 0
    for admin in self.__spectators:
      response += admin + "\n"
      i += 1

    return response

  def add_user(self, spectator, users):
    '''
    Label user as a specator if they are in the channel and not already on the list
    '''
    response = ""
    user_found = False
    for user in users:
      name = user.get("name")
      if name == spectator and not spectator in self.__spectators:
        user_found = True
    
    if user_found:
      self.__spectators.append(spectator)
      response = spectator + " is now a spectator."
    else:
      response = "Could not make " + spectator + " a specatator."

    return response

  def get_count(self):
    return len(self.__spectators)

  def is_spectator_user(self, name):
    is_spectator = False
    if name in self.__spectators:
        is_spectator = True

    return is_spectator


def main():
  pass

if __name__ == '__main__':
  main()
