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
from management import Spectators
from management import Presets

SLACK_BOTS_ALLOWED = True

# admin commands
START_TOURNY = "start"
STOP_TOURNY = "stop"
NEXT_ROUND = "next"
RESET_MATCH = "reset"
HANDLE_ADMIN = "admin"
MAKE_WATCH = "watch"
HANDLE_PRESET = "preset"

# user commands
HELP_COMMAND = "help"
PRINT_TOURNY = "show"
REPORT_WIN = "win"
REPORT_LOSS = "loss"



class Client():
  '''
  This class listens to the Slack Messaging Api and responds.
  '''

  def __init__(self, bot_access_token):
    self.__tournys = TournyHelper()
    self.__client = SlackClient(bot_access_token)
    self.__access_token = bot_access_token
    self.__admins = Mediators()
    self.__spectators = Spectators()
    self.__presets = Presets()

  def get_client(self):
    return self.__client

  def set_client(self):
    del self.__client
    self.__client = SlackClient(self.__access_token)

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
    elif self.__tournys.is_tourny_in_progress():
      response =  "Another tournament is in progress.\nSend the *stop* command to terminate."
    else:
      self.__tournys.clear_players()
      for member_id in members:
        # retrieve user info so we can get profile
        member = self.get_user_porfile(member_id)
        is_bot = member.get('is_bot')
        name = member.get('name')
        is_spectator = self.__spectators.is_spectator_user(name)
        if (not is_bot or SLACK_BOTS_ALLOWED) and not is_spectator:
          # only add real users that are not spectators
          self.__tournys.add_player(member)

      if not is_doubles:
        response = self.__tournys.start_singles(self.__presets.get_all())
      else:
        response = self.__tournys.start_doubles(self.__presets.get_all())

    return response

  def destroy(self):
    self.__tournys.clear_games()
    return "The tournament was destroyed."

  def __add_admin(self, name):
    users = []
    user_ids = self.get_channel_users(self.__tournys.get_current_channel())
    for user_id in user_ids:
      users.append(self.get_user_porfile(user_id))

    return self.__admins.add_user(name, users)

  def __add_spectator(self, name):
    users = []
    user_ids = self.get_channel_users(self.__tournys.get_current_channel())
    for user_id in user_ids:
      users.append(self.get_user_porfile(user_id))

    return self.__spectators.add_user(name, users)

  def __add_preset(self, name):
    users = []
    user_ids = self.get_channel_users(self.__tournys.get_current_channel())
    for user_id in user_ids:
      users.append(self.get_user_porfile(user_id))

    return self.__presets.add_user(name, users)

  def admin_command(self, user_name):
    '''
    These commands can only be used by administrators of the channel.
    '''
    response = ""
    command = self.__tournys.get_current_command()
    channel = self.__tournys.get_current_channel()
    if command.startswith(START_TOURNY):
      doubles = ""
      parts = command.split()
      size = len(parts)
      if size >= 2:
        # possible doubles
        doubles = parts[1]
        
      is_doubles = doubles == "doubles"
      populate_response = self.populate(is_doubles) 
      response = "Generating tournament bracket...\n"
      response += populate_response + "\n"
      response += self.__tournys.get_tourny()

    if command.startswith(STOP_TOURNY):
      destroy_response = self.destroy() 
      response = "Destroying tournament bracket...\n"
      response += destroy_response

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
        response = "Provide a handle to reset the match."

    if command.startswith(NEXT_ROUND):
      response = "Advancing to the next round...\n"
      response += self.__tournys.next_round() + "\n"
      response += self.__tournys.get_tourny()
    
    if command.startswith(REPORT_WIN):
      parts = command.split()
      if len(parts) >= 2:
        # potential handle was provided for disqualification
        handle = parts[1]
        win_response = self.__tournys.report_win(handle)
        response = "Reproting win for " + handle + "...\n" 
        response += win_response + "\n"
        response += self.__tournys.get_tourny()
      else: 
        response = "Provide a handle to win the match."

    if command.startswith(REPORT_LOSS):
      parts = command.split()
      if len(parts) >= 2:
        # potential handle was provided for disqualification
        handle = parts[1]
        loss_response = self.__tournys.report_loss(handle)
        response = "Reproting loss for " + handle + "...\n" 
        response += loss_response + "\n"
        response += self.__tournys.get_tourny()
      else: 
        response = "Provide a handle to lose the match."
   
    if command.startswith(HANDLE_ADMIN):
      response = ""
      parts = command.split()
      count = len(parts)
      if count == 1 and self.__admins.get_count() == 0:
        response = self.__add_admin(user_name)
      elif count >= 2:
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = self.__admins.list_users()
        elif option.startswith("clear"):
          response = self.__admins.clear_users()
        else:
          options = parts[1:]
          for name in options:
            response += self.__add_admin(name)
            response += "\n"
      else:
        response = "Provide the admin handle."

    if command.startswith(MAKE_WATCH):
      response = ""
      parts = command.split()
      count = len(parts)
      if count >= 2:
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = self.__spectators.list_users()
        elif option.startswith("clear"):
          response = self.__spectators.clear_users()
        else:
          options = parts[1:]
          for name in options:
            response += self.__add_spectator(name)
            response += "\n"
      else:
        response = "Provide the spectator handle."

    if command.startswith(HANDLE_PRESET):
      response = ""
      parts = command.split()
      count = len(parts)
      if count >= 2:
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = self.__presets.list_users()
        elif option.startswith("clear"):
          response = self.__presets.clear_users()
        else:
          options = parts[1:]
          for name in options:
            response += self.__add_preset(name)
            response += "\n"
      else:
        response = "Provide the preset handle."

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

    if command.startswith(REPORT_LOSS):
      response = "Reporting a loss...\n"
      response += self.__tournys.report_loss(user) + "\n"
      response += self.__tournys.get_tourny()

    return response

  def handle_command(self, user, command, channel):
    """
      Recieves commands directed to the bot and determins if they
      are valid commands. If so, then acts on teh commands. If not,
      returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
      "* command."

    self.__tournys.set_current_command(user, command, channel)

    user_profile = self.get_user_porfile(user)
    name = user_profile['name']
    is_owner_profile = user_profile['is_owner']
    if self.__admins.get_count() == 0 and is_owner_profile:
      self.__add_admin(name)   # automatically add owner as admin

    is_admin = self.__admins.is_admin_user(name) or is_owner_profile
    is_owner = self.__admins.is_owner_user(name) or is_owner_profile
    owner_exists = self.__admins.get_owner() != ""
    is_admin_command_bool = self.is_admin_command(self.__tournys.get_current_command())
    if is_admin_command_bool and not is_admin:
      response = "Only an admin can use this command."
    elif command == HANDLE_ADMIN and (not is_owner and owner_exists):
      response = "Only the channel owner can use this command."
    elif is_admin_command_bool or command.startswith(HANDLE_ADMIN):
      admin_response = self.admin_command(name)
      if admin_response != "":
        response = admin_response
    else:
      user_response = self.user_command()
      if user_response != "":
        response = user_response

    self.__client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

  def is_admin_command(self, command):
    command_has_parts = len(command.split()) > 1
    is_admin_command = command.startswith(START_TOURNY) or \
      command.startswith(STOP_TOURNY) or \
      command.startswith(NEXT_ROUND) or \
      command.startswith(RESET_MATCH) or \
      command.startswith(MAKE_WATCH) or \
      command.startswith(HANDLE_PRESET) or \
      (command.startswith(REPORT_LOSS) and command_has_parts) or \
      (command.startswith(REPORT_WIN) and command_has_parts)

    return is_admin_command


class Handler():
  '''
  This class holds the the team connection
  '''

  def __init__(self):
    self.__team = Client(os.environ.get('SLACK_BOT_TOKEN'))
    self.__connect(self.__team)

  def __connect(self, slack_team):
    client = slack_team.get_client()
    if client.rtm_connect():
      print("MatchBot is reading events!")
    else:
      # delete the entery from the db maybe
      print("Connection failed. Invalid Slack token or bot ID")

  def reconnect(self, slack_team):
    slack_team.set_client()
    client = slack_team.get_client()
    if client.rtm_connect():
      print("MatchBot is reading events again!")
    else:
      # delete the entery from the db maybe
      print("Connection failed. Invalid Slack token or bot ID")

  def get_team(self):
    return self.__team