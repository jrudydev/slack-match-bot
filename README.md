# Slack Match Bot ![alt text](https://github.com/peperodo/slack-match-bot/blob/match-dev/img/mei.jpg "Logo Title Text 1")
Slack MatchBot makes a list of users in a channel and generates a single elimination tournament bracket.

## Setup Local Environment
```
~$ git clone git@github.com:peperodo/slack-match-bot.git
~$ virtualenv env
~$ source env/bin/activate
(env) ~$ pip install slackclient
(env) ~$ cd ~/slack-match-bot
```
## Export Environment Variables
Find the **Slack API Key_** in the bot configuration section under **Integration Setting -> API Token**
```
(env) ~$ /slack-match-bot: export SLACK_BOT_TOKEN='slack-api-token-goes-here'
(env) ~$ /slack-match-bot: python utils/print_bot_id.py
> could not find bot user with the name matchbot
> could not find bot user with the name matchbot
> The matchbot BOT_ID is: BA3GH56Y   #returned by slack api call
> could not find bot user with the name matchbot
(env) ~$ /slack-match-bot: export BOT_ID='bot-id-returned-from-script'
```
> **SLACK_BOT_TOKEN** should be exported before running the `print_bot_id.py` script.
> then, export the returned string as **BOT_ID** before moving on.

## Run Local Bot
```
(env) ~$ /slack-match-bot: python bot/matchbot.py
> MatchBot connected and running!
```
# Slack Client
It is easy and fast to get a tournament started with MatchBot.

## Setup
1. Create a Slack team (skip this step if you already have a team in mind).
2. Login and add a custom integration to configure a bot named matchbot.
3. Invite matchbot to the team.
4. Create a channel for the tournament.
5. Invite matchbot and more friends to the channel.
6. Complete steps listed above to '**Run Local Bot**'.


## Commands
> @matchbot [COMMAND] 

|COMMAND|DESCRIPTION                 |OPTIONS                       | ADMIN | OWNER |
|:-----:|----------------------------|:----------------------------:|:-----:|:-----:|
|help   |Print a readme file         |None                          |       |       |
|start  |Generate tournament         |[OPTION]  Ex: doubles         |X      |       |
|boot   |Disqualify player           |[HANDLE]  Ex: slackbot        |X      |       |
|reset  |Reset match                 |[HANDLE]  Ex: slackbot        |X      |       |
|next   |Move to next round          |None                          |X      |       |
|admin  |Handle admin roles          |[OPTION]  Ex: show            | 	    |X      |
|show   |Print tournament bracket    |None                          |       |       |
|win    |Report a win                |None                          |       |       |

---
### help
Options: None

Example:
```
@matchbot help
```

Description: Pull up more information about how to use MatchBot.

---
### start (Owner & Admin Only)
Options: [OPTION] = singles | doubles

Example:
```
@matchbot start
```

Description: Generate a tournament from all the players in the room.

---
### boot (Owner & Admin Only)
Options: [HANDLE] = (any handle for a player in the current round)

Example:
```
@matchbot boot slackbot
```

Description: Disqualify a player with matching slack handle.

---
### reset (Owner & Admin Only)
Options: [HANDLE] = (any handle for a player in the current round)

Example:
```
@matchbot reset slackbot
```

Description: Reset the match of player with matching slack handle.

---
### next (Owner & Admin Only)
Options: None

Example:
```
@matchbot next
```

Description: Use to advance to the next round.

---
### admin (Owner Only)
Options: [OPTIONS] = slackbot | show | clear

Example:
```
@matchbot admin show
```

Description: Use to give user admin privileges.

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
