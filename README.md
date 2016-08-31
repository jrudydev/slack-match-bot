# Slack Match Bot
Slack MatchBot makes a list of users in a channel and generates a single elimination tournament bracket.

## Setup Virtual Environment
```
$ cd slack-match-bot
$ virtualenv matchbot
$ source matchbot/bin/activate
(matchbot)$ pip install slackclient
```
## Export Environment Veriables
Find the Slack API key in the bot configuration section under Integration Setting -> API Token
```
(matchbot)$ export SLACK_BOT_TOKEN='slack api token goes here'
(matchbot)$ python print_bot_id.py
> The matchbot BOT_ID is: BA3GH56Y #returned by slack api call
(matchbot)$ export BOT_ID='bot id returned by script'
```
> SLACK_BOT_TOKEN should be exported before running the print_bot_id.py script.
> then, export the returned string as BOT_ID before moving on.

## Run Local Bot Server
```
(matchbot)$ python matchbot.py
> MatchBot connected and runing!
```
# Slack Client
MatchBot makes it easy to setup whether you are on the web or native aplication.

## Setup
- Invite matchbot and more friends

## Commands
> @matchbot [COMMAND] 

|COMMAND|DESCRIPTION                 |OPTIONS                       |
|-------|----------------------------|------------------------------|
|help   |Print a readme file         |[COMMAND] Ex: help start      |
|start  |Generate tournament         |None                          |
|show   |Print tournmanet Bracket    |[ROUND] [MATCH] Ex: show 1 4 |  
|win    |Report a win                |None                          |

---
### help
Options: [COMMAND] = start | show | win

Example:
```
@matchbot help win
```

Description: Use this command to pull up more information about how to use MatchBot.

---
### start
Options: None

Example:
```
@matchbot start
```

Description: Use this command to generate a tournament from all the players in the room.

---
### show
Options: [ROUND] = INT, [MATCH] = INT

Example:
```
@matchbot show 1 4
```

Description: Use this command to print a match, round, or entire tree.

---
### win
Options: None

Example:
```
@matchbot win
```

Description: Use this command to report a win.

