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
from tourny import Tourny
from player import Player

BOT_ID = os.environ.get("BOT_ID") 
AT_BOT = "<@" + BOT_ID  + ">"
SLACK_BOTS_ALLOWED = False

# admin commands
START_TOURNY = "start"
REPORT_QUIT = "boot"
NEXT_ROUND = "next"

# user commands
HELP_COMMAND = "help"
PRINT_TOURNY = "show"
REPORT_WIN = "win"

tourny = Tourny()
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

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

def add_player_to_tourny(member_info):
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

  tourny.add(Player(member_info["id"], member_info["name"], first_name, last_name))

def populate_tourny(bot_channel):
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
        add_player_to_tourny(member)

    response = tourny.start()

  return response

def handle_admin_command(admin_command, bot_channel):
  '''
  These commands can only be used by administrators of the channel.
  '''
  response = ""
  if admin_command.startswith(START_TOURNY):
    populate_response = populate_tourny(bot_channel)    
    response = "Generating tournament bracket...\n"
    response += populate_response + "\n"
    response += tourny.get_printed()

  if admin_command.startswith(REPORT_QUIT):
    parts = admin_command.split()
    if len(parts) >= 2:
      # potential handle was provided for disqualification
      handle = parts[1]
      boot_response = tourny.boot(handle)
      response = "Disqualifying " + handle + "...\n" 
      response += boot_response + "\n"
      response += tourny.get_printed()
    else: 
      response = "Provide and handle to disqualify."

  if admin_command.startswith(NEXT_ROUND):
    response = "Advancing to the next round...\n"
    response += tourny.next() + "\n"
    response += tourny.get_printed()

  return response

def handle_command(user, command, channel):
  """
    Recieves commands directed to the bot and determins if they
    are valid commands. If so, then acts on teh commands. If not,
    returns back what it needs for clarification.
  """
  response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
    "* command with numbers, deliminated by spaces."

  user_profile = get_user_porfile(user)
  is_admin = user_profile.get("is_admin")
  if command.startswith(START_TOURNY) or \
      command.startswith(REPORT_QUIT) or \
      command.startswith(NEXT_ROUND):
    if is_admin:
      admin_response = handle_admin_command(command, channel)
      if admin_response != "":
        response = admin_response
    else:
      response = "Must be an admin to use this command."
  
  if command.startswith(HELP_COMMAND):	
    response = "Sure... write more code then I can do that!"

  if command.startswith(PRINT_TOURNY):
    response = "Printing tournament bracket...\n"
    response += tourny.get_printed()
    
  if command.startswith(REPORT_WIN):
    response = "Reporting a win...\n"
    response += tourny.win(user) + "\n"
    response += tourny.get_printed()

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
