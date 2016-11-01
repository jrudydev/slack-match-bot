# Slack Match Bot ![alt text](https://github.com/peperodo/slack-match-bot/blob/match-dev/img/mei.jpg "Logo Title Text 1")
Slack MatchBot makes a list of users in a channel and generates a single elimination tournament bracket.

## Features
```start``` and populate with channel members.
- Users can opt-in via the ```join``` command, also opt-out with ```boot``` if necessary.
- Begin the tournament by sending ```start``` and end it with```stop```.
- Self-reported match results with the ```win``` & ```loss``` commands.
- Admins have full control over the state of the tournament for corrections.

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
2. Log in and add a custom integration to configure a bot named matchbot.
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
|help   |Documentation link          |None                          |       |       |
|show   |Print current round         |None                          |       |       |
|win    |Report a win                |(Admin Options)               |       |       |
|loss   |Report a loss               |(Admin Options)               |       |       |
|join   |Opt-in of open tourney      |(Admin Options)       |       |       |
|boot   |Opt-out of open tourney     |(Admin Options)               |       |       |
|start  |Generate tournament         |[TYPE]  Ex: doubles           |X      |       |
|stop   |Destroy the tournament      |None                          |X      |       |
|reset  |Reset player match          |[HANDLE]  Ex: slackuser       |X      |       |
|next   |Advance to next round       |None                          |X      |       |
|admin  |Handle admin roles          |[OPTION]  Ex: show            | 	    |X      |


---
### help
**_Options:_** None

Example:
```
@matchbot help
```

**Description:** Pull up more information about how to use MatchBot with a link to the documentation.

---
### show
**_Options:_** None

Example:
```
@matchbot show
```

**Description:** Print the matches for the current round. The round is automatically shown after running other commands that modify the tournament.

---
### win
**_Options:_** None

Example:
```
@matchbot win
```

**_Admin Options:_** [HANDLE] = Ex: slackuser

Example:
```
@matchbot win slackuser
```

**Description:** Report a win for the sender. Once the win is registered, the game is complete and becomes immutable. For corrections contact an admin user. Admin users can pass a handle as and argument and register a win for the user.

---
### loss
**_Options:_** None

Example:
```
@matchbot loss
```

**_Admin Options:_** [HANDLE] = Ex: slackuser

Example:
```
@matchbot loss slackuser
```

**Description:** Report a loss for the sender. Once the loss is registered, the game is complete and becomes immutable. For corrections contact an admin user. Admin users can pass a handle to this command and register a loss for the user.

---
### join
**_Options:_** None

Example:
```
@matchbot join
```

**_Admin Options:_** [HANDLE] = Ex: slackuser

Example:
```
@matchbot join slackuser
```

**Description:** Add the sender as a participant. Admin users can pass a handle as and argument to register the join for the user.

---
### boot
**_Options:_** None

Example:
```
@matchbot boot
```

**_Admin Options:_** [HANDLE] = Ex: slackuser

Example:
```
@matchbot boot slackuser
```

**Description:** Remove the sender as a participant. Admin users can pass a handle as and argument to remove the user.

---
### start (Owner & Admin Only)
**_Options:_** [OPTION] = singles | doubles

Examples:
```
@matchbot start
@matchbot start doubles
```

**Description:** Generate a singles or doubles tournament by randomly selecting a player in the room. With presets, the presets list will be used to populate the tournament without randomizing.

---
### stop (Owner & Admin Only)
**_Options:_** None

Example:
```
@matchbot stop
```

**Description:** Destroys the tournament in order to start a new one. This command is a safe gaurd from losing all data if the *start* command is used while a tournament is in progress.

---
### reset (Owner & Admin Only)
**_Options:_** [HANDLE] = (handle for any player in the current round)

Example:
```
@matchbot reset slackuser
```

**Description:** Reset the match of player with matching slack handle. The match will go revert back to the 'To Be Determined' state.

---
### next (Owner & Admin Only)
**_Options:_** None

Example:
```
@matchbot next
```

**Description:** Use to advance to the next round. All matches for the current round most be complete or bye games. To forfeit a player user the ```boot``` command.

---
### admin (Owner Only)
**_Options:_** [OPTIONS] = slackuser | show | clear | (None)

Examples:
```
@matchbot admin
@matchbot admin slackuser
@matchbot admin show
@matchbot admin clear
```

**Description:** Use to give user admin privileges., show a list, and clear it. If the slack does not give users ownership of channels, send the ```admin``` command with no arguments.
