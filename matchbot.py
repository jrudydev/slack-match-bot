#!/usr/bin/python

import os
import json
from slackclient import SlackClient
import time
from tourny import Tourny
from player import Player

BOT_ID = os.environ.get("BOT_ID") 

# constants
AT_BOT = "<@" + BOT_ID  + ">"

# admin commands
START_TOURNY = "start"
REPORT_QUIT = "boot"
NEXT_ROUND = "next"

# user commmands
HELP_COMMAND = "help"
PRINT_TOURNY = "show"
REPORT_WIN = "win"

tourny = Tourny()
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def __get_bot_channel_id():
  bot_channel_id = None
  api_call = slack_client.api_call("channels.list")
  if api_call.get('ok'):
    # retrieve all channels so we can find our bot
    channels = api_call.get('channels')
    for channel in channels:
      if 'is_member' in channel and channel.get('is_member') == True:
        bot_channel_id = channel.get('id')
        print "Bot channel found."

  return bot_channel_id

def __get_user_porfile(user_id):
  user = {}
  api_call = slack_client.api_call("users.info", user=user_id)
  if api_call.get('ok'):
    user = api_call.get('user')

  return user

def __get_channel_users(bot_channel_id):
  users = []
  api_call = slack_client.api_call("channels.info", channel=bot_channel_id)
  if api_call.get('ok'):
    # retrieve channel info so we can find all the members
    users = api_call.get('channel').get('members')

  return users

def populate_tourny():
  channel_id = __get_bot_channel_id()
  if not channel_id:
    print "Bot not a member of any channels."
    return

  members = __get_channel_users(channel_id)
  for member_id in members:
    # retrieve user info so we can get profile
    member_info = __get_user_porfile(member_id)
    if 'profile' in member_info:
      profile = member_info.get('profile')
      first_name = ""
      if "first_name" in profile:
        first_name = profile.get("first_name")
      last_name = ""
      if "last_name" in profile:
        last_name = profile.get("last_name")

      tourny.add(Player(member_info["id"], member_info["name"], first_name, last_name))

  tourny.start()

def handle_admin_command(admin_command):
  admin_response = ""
  if admin_command.startswith(START_TOURNY):
    populate_tourny()    
    admin_response = "Generating tournament bracket...\n" + tourny.get_printed()

  if admin_command.startswith(REPORT_QUIT):
    parts = admin_command.split()
    if len(parts) >= 2:
      handle = parts[1]
      response = tourny.boot(handle)
      admin_response = "Disqualifying " + handle + "...\n" 
      admin_response += response + "\n" + tourny.get_printed()
    else: 
      admin_response = "Provide and handle to disqualify."

  if admin_command.startswith(NEXT_ROUND):
    admin_response = "Trying to call advance to next round.\n"
    admin_response += tourny.next()

  return admin_response

def handle_command(user, command, channel):
  """
    Recieves commands directed to the bot and determins if they
    are valid commands. If so, then acts on teh commands. If not,
    returns back what it needs for clarification.
  """
  response = "Not sure what you mean. Use the *" + HELP_COMMAND + \
    "* command with numbers, deliminated by spaces."

  user_profile = __get_user_porfile(user)
  is_admin = user_profile.get("is_admin")
  if command.startswith(START_TOURNY) or \
      command.startswith(REPORT_QUIT) or \
      command.startswith(NEXT_ROUND):
    if is_admin:
      admin_response = handle_admin_command(command)
      if admin_response != "":
        response = admin_response
    else:
      response = "Must be an admin to use this command."
  
  if command.startswith(HELP_COMMAND):	
    response = "Sure... write more code then I can do that!"
  if command.startswith(PRINT_TOURNY):
    response = "Printing tournament bracket...\n" + tourny.get_printed()
  if command.startswith(REPORT_WIN):
    response = "Reporting win...\n" + tourny.win(user)

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
