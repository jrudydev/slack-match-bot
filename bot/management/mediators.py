#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: This object manages the admin users for the bot. You can add
# users, list them, and clear the entire list. There is also a convenience
# method to check if a user is an admin.

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
    
    i = 0
    for admin in self.__admins:
      response += admin
      if i == 0:
        response += " (Owner)"
      response += "\n"
      i += 1

    return response

  def add_user(self, admin, users):
    '''
    Promote user to admin if they are in the channel and not already on the list
    '''
    response = ""
    user_found = False
    for user in users:
      name = user.get_handle()
      if name == admin and not admin in self.__admins:
        user_found = True
    
    if user_found:
      self.__admins.append(admin)
      response = admin + " is now an admin."
    else:
      response = "Could not make " + admin + " an admin."

    return response

  def get_owner(self):
    name = ""
    if len(self.__admins) > 0:
      name = self.__admins[0]

    return name

  def get_count(self):
    return len(self.__admins)

  def is_admin_user(self, name):
    is_admin = False
    if name in self.__admins:
        is_admin = True

    return is_admin

  def is_owner_user(self, name):
    is_owner = False
    if name == self.get_owner():
      is_owner = True

    return is_owner


def main():
  pass

if __name__ == '__main__':
  main()