#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: This object manages the admin users for the bot. You can add
# users, list them, and clear the entire list. There is also a convenience
# method to check if a user is an admin by passing the profile.

class Mediators():
  '''
  This class contains a list of users with admin privileges
  '''

  def __init__(self):
  	self.__admins = []

  def clear_users(self):
    del self.__admins[:]

    return "Removing all admins."

  def list_users(self):
    response = "Admins:\n"
    if len(self.__admins) == 0:
      response += "None"

    for admin in self.__admins:
      response += admin + "\n"

    return response

  def add_user(self, admin, channel, users):
    '''
    Promote user to admin if they are in the channel and not already on the list
    '''
    response = ""
    user_found = False
    for user in users:
      name = user.get("name")
      if name == admin and not admin in self.__admins:
        user_found = True
    
    if user_found:
      self.__admins.append(admin)
      response = admin + " is now an admin."
    else:
      response = "Could not make " + admin + " an admin."

    return response

  def is_admin_user(self, profile):
    '''
    Check profile for is_owner flag and also list of admins
    '''
    is_admin = False
    if profile.get("is_owner") or profile.get("name") in self.__admins:
        is_admin = True

    return is_admin


def main():
  pass

if __name__ == '__main__':
  main()