#!/usr/bin/python

# Created by: JRG
# Date: Sept 18, 2016
#
# Description: This object manages the preset users in the tournament. You can add
# users, list them, and clear the entire list.

class Presets():
  '''
  This class contains a list of users that are perset
  '''

  def __init__(self):
  	self.__presets = []

  def clear_users(self):
    del self.__presets[:]

    return "Removing all presets."

  def list_users(self):
    response = "Presets:\n"
    if len(self.__presets) == 0:
      response += "None"
    
    for preset in self.__presets:
      response += preset + "\n"

    return response

  def add_user(self, preset, users):
    '''
    Label user as a preset if they are in the channel and not already on the list
    '''
    response = ""
    user_found = False
    for user in users:
      name = user.get_handle()
      if name == preset and not preset in self.__presets:
        user_found = True
    
    if user_found:
      self.__presets.append(preset)
      response = preset + " is now preset."
    else:
      response = "Could not add " + preset + " as a preset."

    return response

  def get_count(self):
    return len(self.__presets)

  def get_all(self):
    return self.__presets


def main():
  pass

if __name__ == '__main__':
  main()
