# Created by: JRG
# Date: Sept 14, 2016
#
# Description: These classes will manage the slack clients. Each client object
# will also have its own tournament helper, team info, and admins list. The teams
# are populated during initialization of the helper class from the sqlite db.

import os
from slackclient import SlackClient
from tournament import TournyHelper
from management import Mediators

SLACK_BOTS_ALLOWED = True

# admin commands
START_TOURNY = "start"
REPORT_QUIT = "boot"
NEXT_ROUND = "next"
RESET_MATCH = "reset"
HANDLE_ADMIN = "admin"

# user commands
HELP_COMMAND = "help"
PRINT_TOURNY = "show"
REPORT_WIN = "win"


class Client():
  '''
  This class listens to the Slack Messaging Api and responds.
  '''

  def __init__(self, bot_access_token):
    self.__tournys = TournyHelper()
    self.__client = SlackClient(bot_access_token)
    self.__admins = Mediators()

  def get_client(self):
    return self.__client

  def get_user_porfile(self, user_id):
    '''
    Return the user information with the slack id provided.
    '''
    user = {}
    api_call = self.__client.api_call("users.info", user=user_id)
    if api_call.get('ok'):
      user = api_call.get('user')

    return user

  def get_channel_users(self, channel_id):
    '''
    Return the channel information with the slack id provided.
    '''
    users = []
    api_call = self.__client.api_call("channels.info", channel=channel_id)
    if api_call.get('ok'):
      # retrieve channel info so we can find all the members
      users = api_call.get('channel').get('members')

    return users

  def populate(self, is_doubles):
    '''
    Use the slack api to first get a list of channels for the team, find the
    one containing matchbot, then get a list of channel memebers, and finally
    create a player object and add it to the tournament.
    '''
    response = "" 
    members = self.get_channel_users(self.__tournys.get_current_channel())
    if len(members) == 0:
      response =  "The channel does not have any members."
    else:
      for member_id in members:
        # retrieve user info so we can get profile
        member = self.get_user_porfile(member_id)
        is_bot = member.get('is_bot')
        if not is_bot or SLACK_BOTS_ALLOWED:
          # only add real users if flag is set
          self.__tournys.add_player(member)

      if not is_doubles:
        response = self.__tournys.start_singles()
      else:
        response = self.__tournys.start_doubles()

    return response

  def admin_command(self):
    '''
    These commands can only be used by administrators of the channel.
    '''
    response = ""
    command = self.__tournys.get_current_command()
    channel = self.__tournys.get_current_channel()
    if command.startswith(START_TOURNY):
      doubles = ""
      parts = command.split()
      if len(parts) >= 2:
        # possible doubles
        doubles = parts[1]
        
      is_doubles = doubles == "doubles"
      populate_response = self.populate(is_doubles) 
      response = "Generating tournament bracket...\n"
      response += populate_response + "\n"
      response += self.__tournys.get_tourny() 

    if command.startswith(REPORT_QUIT):
      parts = command.split()
      if len(parts) >= 2:
        # potential handle was provided for disqualification
        handle = parts[1]
        boot_response = self.__tournys.boot_slot(handle)
        response = "Disqualifying " + handle + "...\n" 
        response += boot_response + "\n"
        response += self.__tournys.get_tourny()
      else: 
        response = "Provide a handle to disqualify."

    if command.startswith(RESET_MATCH):
      parts = command.split()
      if len(parts) >= 2:
        # potential handle was provided for disqualification
        handle = parts[1]
        reset_response = self.__tournys.reset_match(handle)
        response = "Resetting " + handle + "'s match...\n" 
        response += reset_response + "\n"
        response += self.__tournys.get_tourny()
      else: 
        response = "Provide a handle to disqualify."

    if command.startswith(NEXT_ROUND):
      response = "Advancing to the next round...\n"
      response += self.__tournys.next_round() + "\n"
      response += self.__tournys.get_tourny()

    if command.startswith(HANDLE_ADMIN):
      response = ""
      parts = command.split()
      if len(parts) >= 2:
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = self.__admins.list_users()
        elif option.startswith("clear"):
          response = self.__admins.clear_users()
        else:
          users = []
          user_ids = self.get_channel_users(self.__tournys.get_current_channel())
          for user_id in user_ids:
            users.append(self.get_user_porfile(user_id))
          response = self.__admins.add_user(option, channel, users)
      else: 
        response = "Provide a handle to disqualify."

    return response

  def user_command(self):
    '''
    These commands can used by anyone in the channel.
    '''
    response = ""
    user = self.__tournys.get_current_user()
    command = self.__tournys.get_current_command()
    if command.startswith(HELP_COMMAND):  
      response = "Get the full list of commands here:\n" + \
        "https://github.com/peperodo/slack-match-bot"

    if command.startswith(PRINT_TOURNY):
      response = "Printing tournament bracket...\n"
      response += self.__tournys.get_tourny()
      
    if command.startswith(REPORT_WIN):
      response = "Reporting a win...\n"
      response += self.__tournys.report_win(user) + "\n"
      response += self.__tournys.get_tourny()

    return response

  def handle_command(self, user, command, channel):
    """
      Recieves commands directed to the bot and determins if they
      are valid commands. If so, then acts on teh commands. If not,
      returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
      "* command with numbers, deliminated by spaces."

    self.__tournys.set_current_command(user, command, channel)

    user_profile = self.get_user_porfile(user)
    is_admin = self.__admins.is_admin_user(user_profile)
    is_admin_command_bool = self.is_admin_command(self.__tournys.get_current_command())
    if is_admin_command_bool and not is_admin:
      response = "Only an admin can use this command."
    elif command == HANDLE_ADMIN and not user_profile.get('is_owner'):
      response = "Only the channel owner can use this command."
    elif is_admin_command_bool:
      admin_response = self.admin_command()
      if admin_response != "":
        response = admin_response
    else:
      user_response = self.user_command()
      if user_response != "":
        response = user_response

    self.__client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

  def is_admin_command(self, command):
    return command.startswith(START_TOURNY) or \
      command.startswith(REPORT_QUIT) or \
      command.startswith(NEXT_ROUND) or \
      command.startswith(RESET_MATCH) or \
      command.startswith(HANDLE_ADMIN)


class Handler():
  '''
  This class holds the array of teams initialized from sqlite table
  '''

  def __init__(self):
    self.team = Client(os.environ.get('SLACK_BOT_TOKEN'))
    self.connect_to_slack()

  def connect_to_slack(self):
    if self.team.get_client().rtm_connect():
      print("MatchBot is reading events!")
    else:
      # delete the entery from the db maybe
      print("Connection failed. Invalide Slack token or bot ID")

  def get_team(self):
    return self.team