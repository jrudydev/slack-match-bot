# Slack Match Bot
Slack MatchBot makes a list of users in a channel and generates a single elimination tournament bracket.

## Setup Local Virtual Environment
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

## Run Local Bot
```
(matchbot)$ python matchbot.py
> MatchBot connected and runing!
```
# Slack Client
MatchBot makes it easy to setup whether you are on the web or native aplication.

## Setup
1. Create a Slack team (skip this step if you already have a team in mind).
2. Login and add a custom integration to configure a bot named matchbot.
3. Invite matchbot to the team.
4. Create a channel for the tournament.
5. Invite matchbot and more friends to the channel.
6. Complete steps listed above to 'Run Local Bot'.


## Commands
> @matchbot [COMMAND] 

|COMMAND|DESCRIPTION                 |OPTIONS                       | ADMIN ONLY |
|:-----:|----------------------------|:----------------------------:|:----------:|
|help   |Print a readme file         |None                          |            |
|start  |Generate tournament         |[OPTION]  Ex: doubles         |x           |
|boot   |Disqualify player           |[HANDLE]  Ex: slackbot        |x           |
|reset  |Reset match                 |[HANDLE]  Ex: slackbot        |x           |
|next   |Move to next round          |None                          |x			 |
|admin  |Handle admin roles          |[OPTION]  Ex: show            |x			 |
|show   |Print tournmanet bracket    |None                          |            |
|win    |Report a win                |None                          |            |

---
### help
Options: None

Example:
```
@matchbot help
```

Description: Pull up more information about how to use MatchBot.

---
### start (Admin Only)
Options: [OPTION] = singles | doubles

Example:
```
@matchbot start
```

Description: Generate a tournament from all the players in the room.

---
### boot (Admin Only)
Options: [HANDLE] = (any handle for a player in the current round)

Example:
```
@matchbot boot slackbot
```

Description: Disqualify a player with matching slack handle.

---
### reset (Admin Only)
Options: [HANDLE] = (any handle for a player in the current round)

Example:
```
@matchbot reset slackbot
```

Description: Reset the match of player with matching slack handle.

---
### next (Admin Only)
Options: None

Example:
```
@matchbot next
```

Description: Use to advance to the next round.

---
### admin (Admin Only)
Options: [OPTIONS] = slackbot | show | clear

Example:
```
@matchbot admin show
```

Description: Use to give user admin privledges.

---
### show
Options: None

Example:
```
@matchbot show
```

Description: Print a match, round, or entire tree.

---
### win
Options: None

Example:
```
@matchbot win
```

Description: Report a win for the sender.
