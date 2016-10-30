# Created by: JRG
# Date: Sept 14, 2016
#
# Description: These classes will manage the slack clients. Each client object
# will also have its own tournament helper, team info, and admins list. The teams
# are populated during initialization of the helper class from the sqlite db.

from slackclient import SlackClient
from tournament import TourneyHelper
from management import Mediators
import re

SLACK_BOTS_ALLOWED = True

# admin commands
OPEN_TOURNEY = "open"
START_TOURNEY = "start"
STOP_TOURNEY = "stop"
NEXT_ROUND = "next"
RESET_MATCH = "reset"
HANDLE_ADMIN = "admin"
MAKE_WATCH = "watch"
HANDLE_PRESET = "preset"

# user commands
HELP_COMMAND = "help"
PRINT_TOURNEY = "show"
REPORT_WIN = "win"
REPORT_LOSS = "loss"
REPORT_JOIN = "join"
REPORT_LEAVE = "leave"


class Client():
  '''
  This class listens to the Slack Messaging Api and responds.
  '''

  def __init__(self, team_info):
    self.__tourneys = TourneyHelper()
    self.__client = SlackClient(team_info.bot_access_token)
    self.__access_token = team_info.bot_access_token
    self.__admins = Mediators()
    self.__info = team_info

  def get_info(self):
    return self.__info

  def get_client(self):
    return self.__client

  def set_client(self):
    del self.__client
    self.__client = SlackClient(self.__access_token)

  def admin_command(self, user_name):
    '''
    These commands can only be used by administrators of the channel.
    '''
    response = ""
    command = self.__tourneys.get_current_command()
    channel = self.__tourneys.get_current_channel()
    tourney = self.__tourneys.get_current_tourney()
    if command.startswith(OPEN_TOURNEY):
      doubles = ""
      parts = command.split()
      if len(parts) >= 2 and not self.__is_slack_shortcode(parts[1]):
        # possible doubles
        doubles = parts[1]

      is_doubles = doubles == "doubl"
      open_response = self.__open_tourney(is_doubles) 
      request = "Opening tournament bracket...\n"
      response = request + open_response
      response += tourney.list_players()

    if command.startswith(START_TOURNEY):
      doubles = ""
      parts = command.split()
      if len(parts) >= 2 and not self.__is_slack_shortcode(parts[1]):
        # possible doubles
        doubles = parts[1]
        
      is_doubles = doubles == "doubles"
      start_response = self.__start_tourney(is_doubles) 
      request = "Generating tournament bracket...\n"
      response = request + start_response + "\n"
      response += self.__tourneys.get_tourney()

    if command.startswith(STOP_TOURNEY):
      request = "Destroying tournament bracket...\n"
      destroy_response = self.__destroy_tourney(tourney) 
      response = request + destroy_response

    if command.startswith(RESET_MATCH):
      parts = command.split()
      if len(parts) >= 2 and not self.__is_slack_shortcode(parts[1]):
        # potential handle was provided for disqualification
        handle = parts[1]
        reset_response = self.__tourneys.reset_match(handle)
        request = "Resetting " + handle + "'s match...\n"
        response = request + reset_response + "\n"
        response += self.__tourneys.get_tourney()
      else: 
        response = "Provide a handle to reset the match."

    if command.startswith(NEXT_ROUND):
      request = "Advancing to the next round...\n"
      next_response = self.__tourneys.next_round()
      response = request + next_response + "\n"
      response += self.__tourneys.get_tourney()
    
    if command.startswith(REPORT_WIN):
      parts = command.split()
      if len(parts) >= 2:
        win_response = ""
        handles = parts[1:]
        for handle in handles:
          if not self.__is_slack_shortcode(handle):
            # potential handle was provided for disqualification
            win_response += self.__tourneys.report_win_with_handle(handle) + "\n"

        if len(handles) == 1:
          request = "Reproting win for " + handle + "...\n"
        else:
          handles_output = " & ".join(handles)
          request = "Reporting wins for " + handles_output + "...\n"
        response = request + win_response + "\n"
        response += self.__tourneys.get_tourney()
      else: 
        response = "Provide a handle to report the win."

    if command.startswith(REPORT_LOSS):
      parts = command.split()
      if len(parts) >= 2:
        loss_response = ""
        handles = parts[1:]
        for handle in handles:
          if not self.__is_slack_shortcode(handle):
            # potential handle was provided for disqualification
            loss_response += self.__tourneys.report_loss_with_handle(handle) + "\n"
        
        if len(handles) == 1:
          request = "Reproting loss for " + handle + "...\n" 
        else:
          handles_output = " & ".join(handles)
          request = "Reporting losses for " + handles_output + "...\n"
        response = request + loss_response + "\n"
        response += self.__tourneys.get_tourney()
      else: 
        response = "Provide a handle to report the loss."
   
    if command.startswith(HANDLE_ADMIN):
      users = tourney.get_channel_users()
      response = ""
      parts = command.split()
      count = len(parts)
      if count == 1 and self.__admins.get_count() == 0:
        response = self.__admins.add_user(user_name, users)
      elif count >= 2 and not self.__is_slack_shortcode(parts[1]):
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = self.__admins.list_users()
        elif option.startswith("clear"):
          response = self.__admins.clear_users()
        else:
          options = parts[1:]
          for name in options:
            response += self.__admins.add_user(name, users)
            response += "\n"
      else:
        response = "Provide the admin handle."

    if command.startswith(REPORT_JOIN):
      response = ""
      parts = command.split()
      count = len(parts)
      if count >= 2 and not self.__is_slack_shortcode(parts[1]):
        # potential handle was provided for participant
        options = parts[1:]
        users = tourney.get_channel_users()
        request = "Players joining the tournament...\n"
        response_parts = []
        for name in options:
          user_id = self.__tourneys.get_current_tourney().get_user_id(name)
          response_parts.append(self.__join_tourney(user_id))
        response += "\n".join(response_parts)
        response = request + response
        response += "\nSend the `join` command to participate."
        response += tourney.list_players()
      else:
        response = "Provide a handle for the participant."

    if command.startswith(HANDLE_PRESET):
      response = ""
      parts = command.split()
      count = len(parts)
      if count >= 2 and not self.__is_slack_shortcode(parts[1]):
        # potential handle was provided for disqualification
        option = parts[1]
        if option.startswith("show"):
          response = tourney.presets.list_users()
        elif option.startswith("clear"):
          response = tourney.presets.clear_users()
        else:
          options = parts[1:]
          users = tourney.get_channel_users()
          for name in options:
            response += tourney.presets.add_user(name, users)
            response += "\n"
      else:
        response = "Provide the preset handle."

    return response

  def user_command(self):
    '''
    These commands can used by anyone in the channel.
    '''
    response = ""
    user = self.__tourneys.get_current_user()
    command = self.__tourneys.get_current_command()
    tourney = self.__tourneys.get_current_tourney()
    if command.startswith(HELP_COMMAND):  
      response = "Get the full list of commands here:\n" + \
        "https://github.com/peperodo/slack-match-bot"

    if command.startswith(PRINT_TOURNEY):
      request = "Printing tournament bracket...\n"
      response = request + self.__tourneys.get_tourney()
      
    if command.startswith(REPORT_WIN):
      request = "Reporting a win...\n"
      win_response = self.__tourneys.report_win(user)
      response = request + win_response + "\n"
      response += self.__tourneys.get_tourney()

    if command.startswith(REPORT_LOSS):
      request = "Reporting a loss...\n"
      loss_response = self.__tourneys.report_loss(user)
      response = request + loss_response + "\n"
      response += self.__tourneys.get_tourney()

    if command.startswith(REPORT_JOIN):
      request = "Player is joining the tournament...\n"
      join_response = self.__join_tourney(user)
      response = request + join_response
      response += "\nSend the `join` command to participate."
      response += tourney.list_players()

    return response

  def handle_command(self, user, command, channel):
    """
      Recieves commands directed to the bot and determins if they
      are valid commands. If so, then acts on teh commands. If not,
      returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the `" + HELP_COMMAND + \
      "` command."

    clean_command = self.__get_clean_options(command)
    self.__tourneys.set_current_command(user, clean_command, channel)
    if len(self.__tourneys.get_current_tourney().get_channel_users()) == 0:
      self.__set_tourney_channel_users()

    user_profile = self.__get_user_porfile(user)
    name = user_profile['name']
    is_owner_profile = user_profile['is_owner']
    if self.__admins.get_count() == 0 and is_owner_profile:
      tourney = self.__tourneys.get_current_tourney()
      self.__admins.add_user(name, tourney.get_channel_users())   # automatically add owner as admin

    is_admin = self.__admins.is_admin_user(name) or is_owner_profile
    is_owner = self.__admins.is_owner_user(name) or is_owner_profile
    owner_exists = self.__admins.get_owner() != ""
    is_admin_command_bool = self.is_admin_command(clean_command)
    if is_admin_command_bool and not is_admin:
      response = "Only an admin can use this command."
    elif clean_command == HANDLE_ADMIN and (not is_owner and owner_exists):
      response = "Only the channel owner can use this command."
    elif is_admin_command_bool or clean_command.startswith(HANDLE_ADMIN):
      admin_response = self.admin_command(name)
      if admin_response != "":
        response = admin_response
    else:
      user_response = self.user_command()
      if user_response != "":
        response = user_response
    
    self.__client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

  def is_admin_command(self, command):
    parts = command.split()
    command_has_parts = len(parts) > 1

    is_admin_command = command.startswith(OPEN_TOURNEY) or \
      command.startswith(START_TOURNEY) or \
      command.startswith(STOP_TOURNEY) or \
      command.startswith(NEXT_ROUND) or \
      command.startswith(RESET_MATCH) or \
      command.startswith(MAKE_WATCH) or \
      command.startswith(HANDLE_PRESET) or \
      (command.startswith(REPORT_LOSS) and command_has_parts) or \
      (command.startswith(REPORT_WIN) and command_has_parts) or \
      (command.startswith(REPORT_JOIN) and command_has_parts)

    return is_admin_command

  def __get_user_porfile(self, user_id):
    '''
    Return the user information with the slack id provided.
    '''
    user = {}
    api_call = self.__client.api_call("users.info", user=user_id)
    if api_call.get('ok'):
      user = api_call.get('user')

    return user

  def __get_channel_users(self, channel_id):
    '''
    Return the channel information with the slack id provided.
    '''
    users = []
    api_call = self.__client.api_call("channels.info", channel=channel_id)
    if api_call.get('ok'):
      # retrieve channel info so we can find all the members
      users = api_call.get('channel').get('members')

    return users

  def __set_tourney_channel_users(self):
    '''
    Use the slack api to first get a list of channel memebers.
    '''
    channel = self.__tourneys.get_current_channel()
    members = self.__get_channel_users(channel)
    self.__tourneys.clear_current()
    for member_id in members:
      # retrieve user info so we can get profile
      member = self.__get_user_porfile(member_id)
      is_bot = member.get('is_bot')
      name = member.get('name')
      if not is_bot or SLACK_BOTS_ALLOWED:
        # only add real users
        self.__tourneys.add_user(member)

  def __get_tourney_channel_users(self):
    tourney = self.__tourneys.get_current_tourney()
    return tourney.get_channel_users()

  def __open_tourney(self, is_doubles):
    '''
    Create the tournaments and prepare to let players join.
    '''
    tourney = self.__tourneys.get_current_tourney()
    if self.__tourneys.is_tourney_in_progress() or tourney.is_joinable:
      return  "Another tournament is in progress.\nSend the `stop` command to terminate."
    
    tourney.is_joinable = True
    self.__set_tourney_channel_users()
    response = ""
    if is_doubles:
      response = "Double elimination tournament is now open."
    else:
      response = "Single elimnination tournament is now open."
    response += "\nSend the `join` command to participate."

    return response

  def __join_tourney(self, user):
    '''
    Allow players to join the tournament.
    '''
    if not self.__tourneys.get_current_tourney().is_joinable:
      return "The tournament is not joinable."
    if self.__tourneys.is_tourney_in_progress():
      return  "Cannot join a tournament in progress."

    self.__set_tourney_channel_users()
    response = self.__tourneys.report_join(user)

    return response

  def __start_tourney(self, is_doubles):
    '''
    Deterimine if the tournament has participants or use channel users to populate the tournament.
    '''
    if self.__tourneys.is_tourney_in_progress():
      return "Another tournament is in progress.\nSend the `stop` command to terminate."

    self.__set_tourney_channel_users()
    response = ""
    if not is_doubles:
      response = self.__tourneys.start_singles()
    else:
      response = self.__tourneys.start_doubles()

    return response

  def __destroy_tourney(self, tourney):
    self.__tourneys.clear_games(tourney)
    return "The tournament was destroyed."

  def __is_slack_shortcode(self, handle):
    response = False
    if handle.startswith("<@"):
      response = True

    return response

  def __get_clean_options(self, command):
    parts = command.split()
    if len(parts) > 1 and parts[0] == ':':
      parts = parts[1:]
    
    # replace all the user shortcodes with the handles if they are in the tournament
    current_tourney = self.__tourneys.get_current_tourney()
    new_parts = []
    for part in parts:
      match = re.search(r'<@(u)([\w\d]+)>', part)
      if match:
        user_id = match.group(1) + match.group(2)
        player = current_tourney.get_user(user_id)
        if player != None:
          new_parts.append(player.get_handle())
        else:
          new_parts.append(part)
      else:
        new_parts.append(part)

    return " ".join(new_parts)


class Handler():
  '''
  This class holds the array of teams initialized from sqlite table
  '''

  def __init__(self):
    self.__teams = []

  def add_team(self, slack_bot_token):
    team_object = SlackTeam(slack_bot_token)
    self.__connect(Client(team_object))

  def __connect(self, slack_team):
    if slack_team.get_client().rtm_connect():
      print("MatchBot is reading events!")
      self.__teams.append(slack_team)
    else:
      print("Connection failed. Invalid Slack token or bot ID.")

  def reconnect(self, slack_team):
    slack_team.set_client()
    self.__connect(slack_team)

  def get_teams(self):
    return self.__teams


class SlackTeam():
  '''
  Placeholder object to mock db
  '''

  def __init__(self, access_token):
    self.bot_access_token = access_token