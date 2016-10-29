#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: MatchBot attemps to intelligently respond to a slack user's
# demands to automate a single elimination bracket. The bot allows participants
# to register their own wins and gives the admin full control of bracket progression.

import socket
import os
import json
import time
from handler import Handler

BOT_ID = os.environ.get("BOT_ID") 
AT_BOT = "<@" + BOT_ID  + ">"

def parse_slack_output(slack_rtm_output):
  """
    The Slack Real Time Messaging API is an events firehose.
    This parsing function returns None unless a messagte is
    directed at the Bot, based on its ID.
  """
  if slack_rtm_output and len(slack_rtm_output) > 0:
    for output in slack_rtm_output:
      if output and 'text' in output and AT_BOT in output['text'] and 'user' in output:
        # return text after the @ mention, whitespace removed
        return output['user'], output['text'].split(AT_BOT)[1].strip(' ').lower(), output['channel']

  return None, None, None


def main():
  READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
  handler = Handler()
  handler.add_team(os.environ.get('SLACK_BOT_TOKEN'))
  teams = handler.get_teams()
  team = teams[0]
  while True:
    client = team.get_client()
    try:
      user, command, channel = parse_slack_output(client.rtm_read())
      if command and channel:
        team.handle_command(user, command, channel)
      time.sleep(READ_WEBSOCKET_DELAY)
    except Exception:
      handler.reconnect(team)
    

if __name__ == '__main__': 
  main()
