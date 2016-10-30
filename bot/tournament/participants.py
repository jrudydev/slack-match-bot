#!/usr/bin/python

# Created by: JRG
# Date: Sept 29, 2016
#
# Description: This object manages the participants in the tournament. You can add
# users, list them, and clear the list. There is also a convenience
# method to check if a user is a already a participant.

class Participants():
  '''
  This class contains a list of users that are participants
  '''

  def __init__(self):
  	self.__handles = []

  def clear_users(self):
    del self.__handles[:]

    return "Removing all participants."

  def add_user(self, player, users):
    '''
    Add user as participant if they are in the channel and not already on the list
    '''
    response = ""
    user_found = False
    for user in users:
      name = user.get_handle()
      if name == player and not player in self.__handles:
        user_found = True
    
    if user_found:
      self.__handles.append(player)
      response = player + " joined the tournament."
    else:
      response = "Could not make " + player + " a participant."

    return response

  def remove_user(self, player, users):
  	'''
  	Use this method to remove players from the participant list before the tournament starts
  	'''
  	response = ""
  	user_found = False
  	i = 0
  	for user in users:
  	  name = user.get("name")
  	  if player in self.__handles:
  	  	user_found = True
  	  	break
  	  else:
  	  	i += i
  	if user_found:
  	  del self.__handles[i]
  	  response = player + " is no longer a participant."
  	else:
  	  response = "Could not remove " + player + " as a participant."

  	return response

  def get_handles(self):
  	return self.__handles

  def get_count(self):
    return len(self.__handles)

  def is_participant(self, name):
    is_participant = False
    if name in self.__handles:
        is_participant = True

    return is_participant


def main():
  pass

if __name__ == '__main__':
  main()