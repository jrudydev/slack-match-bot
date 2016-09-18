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
7. Complete steps listed above to '**Run Local Bot**'.
8. Start the tournament by typing ```@matchbot start```


> Can't run the start command without admin?
> If you are not the owner of the channel, type ```@matchbot admin```
 
 
## Commands
> @matchbot  |COMMAND| |ARGUMENTS|

|COMMAND|DESCRIPTION                 |ARGUMENTS                     | ADMIN | OWNER |
|:-----:|----------------------------|:----------------------------:|:-----:|:-----:|
|help   |Print a readme file         |None                          |       |       |
|start  |Generate tournament         |[TYPE]  Ex: doubles           |X      |       |
|boot   |Disqualify player           |[HANDLE]  Ex: slackuser       |X      |       |
|reset  |Reset player match          |[HANDLE]  Ex: slackuser       |X      |       |
|next   |Advance to next round       |None                          |X      |       |
|watch  |Handle spectator users      |[OPTION]  Ex: slackuser       |X	    |       |
|preset |Handle preset placement     |[OPTION]  Ex: clear           |X	    |       |
|admin  |Handle admin roles          |[OPTION]  Ex: show            | 	    |X      |
|show   |Print current round         |None                          |       |       |
|win    |Report a win                |None                          |       |       |

---
### help
Options: None

Example:
```
@matchbot help
```

Description: Pull up more information about how to use MatchBot and a link to the documentation.

---
### start (Owner & Admin Only)
Options: [OPTION] = singles | doubles

Example:
```
@matchbot start
@matchbot start doubles
```

Description: Generate a singles or doubles tournament by randomly selecting a player in the room. With presets, the presets list will be used to populate the tournament without randomizing.

---
### boot (Owner & Admin Only)
Options: [HANDLE] = (handle for any player in the current round)

Example:
```
@matchbot boot slackuser
```

Description: Disqualify a player with matching slack handle. The opponent will automatically be awarded the win and the match will be complete.

---
### reset (Owner & Admin Only)
Options: [HANDLE] = (handle for any player in the current round)

Example:
```
@matchbot reset slackuser
```

Description: Reset the match of player with matching slack handle. The match will go revert back to the 'To Be Determined' state.

---
### next (Owner & Admin Only)
Options: None

Example:
```
@matchbot next
```

Description: Use to advance to the next round. All matches for the current round most be complete or bye games. To forfeit a player user the ```boot``` command.

---
### watch (Owner & Admin Only)
Options: [OPTIONS] = slackuser | show | clear

Example:
```
@matchbot watch slackuser
@matchbot watch show
@matchbot watch clear
```

Description: Use to make a spectator, show a list, and clear it. Spectators can be in a channel while not having to participate in the tournament.

---
### preset (Owner & Admin Only)
Options: [OPTIONS] = slackuser | show | clear

Example:
```
@matchbot presets slackuser
@matchbot presets show
@matchbot presets clear
```

Description: Use to set a preset, show a list, and clear it. The bracket will not be random when after assigning presets, instead it populates from the presets and will be positioned in order.

---
### admin (Owner Only)
Options: [OPTIONS] = slackuser | show | clear | (None)

Examples:
```
@matchbot admin
@matchbot admin slackuser
@matchbot admin show
@matchbot admin clear
```

Description: Use to give user admin privileges., show a list, and clear it. If the slack does not give users ownership of channels, send the ```admin``` command with no arguments.

---
### show
Options: None

Example:
```
@matchbot show
```

Description: Print the matches for the current round. The round is automatically shown after running other commands that modify the tournament.

---
### win
Options: None

Example:
```
@matchbot win
```

Description: Report a win for the sender. Once the win is registered, the game is complete and becomes immutable. For corrections contact an admin user.
