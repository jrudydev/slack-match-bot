#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: MatchBot attemps to intelligently respond to a slack user's
# demands to automate a single elimination bracket. The bot allows participants
# to register their own wins and gives the admin full control of bracket progression.

import os
import json
from slackclient import SlackClient
import time
from tourny_helper import TournyHelper
from mediators import Mediators

BOT_ID = os.environ.get("BOT_ID") 
AT_BOT = "<@" + BOT_ID  + ">"
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

tournys = TournyHelper()
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
admins = Mediators()

def get_user_porfile(user_id):
  '''
  Return the user information with the slack id provided.
  '''
  user = {}
  api_call = slack_client.api_call("users.info", user=user_id)
  if api_call.get('ok'):
    user = api_call.get('user')

  return user

def get_channel_users(bot_channel_id):
  '''
  Return the channel information with the slack id provided.
  '''
  users = []
  api_call = slack_client.api_call("channels.info", channel=bot_channel_id)
  if api_call.get('ok'):
    # retrieve channel info so we can find all the members
    users = api_call.get('channel').get('members')

  return users

def populate(bot_channel, is_doubles):
  '''
  Use the slack api to first get a list of channels for the team, find the
  one containing matchbot, then get a list of channel memebers, and finally
  create a player object and add it to the tournament.
  '''
  response = "" 
  members = get_channel_users(bot_channel)
  if len(members) == 0:
    response =  "The channel does not have any members."
  else:
    for member_id in members:
      # retrieve user info so we can get profile
      member = get_user_porfile(member_id)
      is_bot = member.get('is_bot')
      if not is_bot or SLACK_BOTS_ALLOWED:
        # only add real users if flag is set
        tournys.add_player(member)

    if not is_doubles:
      response = tournys.start_singles()
    else:
      response = tournys.start_doubles()

  return response
  
def is_admin_command(tourny_command):
  return tourny_command.startswith(START_TOURNY) or \
      tourny_command.startswith(REPORT_QUIT) or \
      tourny_command.startswith(NEXT_ROUND) or \
      tourny_command.startswith(RESET_MATCH) or \
      tourny_command.startswith(HANDLE_ADMIN)

def admin_command(run_command, bot_channel):
  '''
  These commands can only be used by administrators of the channel.
  '''
  response = ""
  if run_command.startswith(START_TOURNY):
    doubles = ""
    parts = run_command.split()
    if len(parts) >= 2:
      # possible doubles
      doubles = parts[1]


    is_doubles = doubles == "doubles"
    populate_response = populate(bot_channel, is_doubles) 
    response = "Generating tournament bracket...\n"
    response += populate_response + "\n"
    response += tournys.get_tourny() 

  if run_command.startswith(REPORT_QUIT):
    parts = run_command.split()
    if len(parts) >= 2:
      # potential handle was provided for disqualification
      handle = parts[1]
      boot_response = tournys.boot_slot(handle)
      response = "Disqualifying " + handle + "...\n" 
      response += boot_response + "\n"
      response += tournys.get_tourny()
    else: 
      response = "Provide a handle to disqualify."

  if run_command.startswith(RESET_MATCH):
    parts = run_command.split()
    if len(parts) >= 2:
      # potential handle was provided for disqualification
      handle = parts[1]
      reset_response = tournys.reset_match(handle)
      response = "Disqualifying " + handle + "...\n" 
      response += reset_response + "\n"
      response += tournys.get_tourny()
    else: 
      response = "Provide a handle to disqualify."

  if run_command.startswith(NEXT_ROUND):
    response = "Advancing to the next round...\n"
    response += tournys.next_round() + "\n"
    response += tournys.get_tourny()

  if run_command.startswith(HANDLE_ADMIN):
    response = ""
    parts = run_command.split()
    if len(parts) >= 2:
      # potential handle was provided for disqualification
      option = parts[1]
      if option.startswith("show"):
        response = admins.list_users()
      elif option.startswith("clear"):
        response = admins.clear_users()
      else:
        users = []
        user_ids = get_channel_users(bot_channel)
        for user_id in user_ids:
          users.append(get_user_porfile(user_id))
        response = admins.add_user(option, bot_channel, users)
    else: 
      response = "Provide a handle to disqualify."

  return response

def user_command(user_handle, run_command):
  '''
  These commands can used by anyone in the channel.
  '''
  response = ""
  if run_command.startswith(HELP_COMMAND):  
    response = "Get the full list of commands here:\n" + \
      "https://github.com/peperodo/slack-match-bot"

  if run_command.startswith(PRINT_TOURNY):
    response = "Printing tournament bracket...\n"
    response += tournys.get_tourny()
    
  if run_command.startswith(REPORT_WIN):
    response = "Reporting a win...\n"
    response += tournys.report_win(user_handle) + "\n"
    response += tournys.get_tourny()

  return response

def handle_command(user, command, channel):
  """
    Recieves commands directed to the bot and determins if they
    are valid commands. If so, then acts on teh commands. If not,
    returns back what it needs for clarification.
  """
  response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
    "* command with numbers, deliminated by spaces."

  tournys.set_current_tourny(channel)

  user_profile = get_user_porfile(user)
  is_admin = admins.is_admin_user(user_profile)
  is_admin_command_bool = is_admin_command(command)
  if is_admin_command_bool and not is_admin:
    response = "Only an admin can use this command."
  elif command == HANDLE_ADMIN and not user_profile.get('is_owner'):
    response = "Only the channel owner can use this command."
  elif is_admin_command_bool:
    admin_response = admin_command(command, channel)
    if admin_response != "":
      response = admin_response
  else:
    user_response = user_command(user, command)
    if user_response != "":
      response = user_response

  slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
  """
    The Slack Real Time Messaging API is an events firehose.
    This parsing function returns None unless a messagte is
    directed at the Bot, based on its ID.
  """
  output_list = slack_rtm_output
  if output_list and len(output_list) > 0:
    for output in output_list:
      if output and 'text' in output and AT_BOT in output['text'] and 'user' in output:
        # return text after the @ mention, whitespace removed
        return output['user'], output['text'].split(AT_BOT)[1].strip(' ').lower(), output['channel']

  return None, None, None


def main():
  READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
  if slack_client.rtm_connect():
    print("MatchBot connected and runing!")
    while True:
      user, command, channel = parse_slack_output(slack_client.rtm_read())
      if command and channel:
        handle_command(user, command, channel)
      time.sleep(READ_WEBSOCKET_DELAY)
  else:
    print("Connection failed. Invalide Slack token or bot ID")

if __name__ == '__main__': 
  main()