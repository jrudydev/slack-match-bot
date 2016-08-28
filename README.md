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
MatchBot makes it easy to setup whether on you are on the web or native aplication.

## Setup
- Create a channel called pingpongtourny
- Invite matchbot and more friends

## Commands
> @matchbot [COMMAND] 

|COMMAND|DESCRIPTION                 |
|-------|----------------------------|
|help   |Print a readme file         |
|start  |Generate tournament         |
|print  |Print tournmanet Bracket    |
|win    |Report a win                |

