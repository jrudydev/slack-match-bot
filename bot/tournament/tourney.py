#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The tourny object will allow the slack bot to create a
# tournament with the users in the channel. It also provides methods to
# prgress the tournament and eventually crown a winner.

from player import Player
from team import Team
from match import Match
from trees import WinnersBracket, LossersBracket
import random

class Tourney:
  '''
  This class provides methods to manage the tournament tree bracket.
  '''

  def __init__(self):
    self.__players = {}
    self.__user_ids = {}
    self.__winners = WinnersBracket()
    self.__losers = LossersBracket()
    self.__is_doubles = False

  def add(self, player):
    self.__players[player.get_user()] = player
    self.__user_ids[player.get_handle()] = player.get_user()
       
  def build_bracket(self, user, is_doubles, presets):
  	self.__is_doubles = is_doubles
    is_random = True
    is_preset = len(presets) > 0
    if is_preset:
      num_players, num_slots = self.__get_number_of_players_and_slots_tuple(presets)
      is_random = False
    else:
      num_players, num_slots = self.__get_number_of_players_and_slots_tuple(self.__players)
    is_odd = num_players % 2 == 1

    if number_of_slots < 2:
      return "There are not enough players."

    if is_doubles and is_odd and is_preset:
      return "There is an odd number of presets."

    response = ""
    team = None
    slots = []
    i = 0
    if is_random:
      players = []
      for key in self.__players:
        if not is_odd or key != user:
          players.append(self.__players[key]) 

      for x in range(len(players)):
        rand_int = random.choice(range(len(players)))
        random_player = players[rand_int]
        del players[rand_int]
       
        self.__populate_team(random_player, team, slots, is_doubles)

      if is_doubles:
      	response = "Doubles bracket randomly generated."
      if not is_doubles = "Singles bracket randomly generated."
    else:
      for handle in presets:
      	user_id = self.__user_ids[handle]
        player = self.__players[user_id]
        self.__populate_team(player, team, slots, is_doubles)

      slots = self.__get_order_preset(slots)
      if is_doubles:
      	response = "Doubles bracket generated from presets."
      if not is_doubles = "Singles bracket generated from presets."
    
    self.__winners.generate(slots, is_random)

    return response

  def __populate_team_with_player(self, player, team, slots, is_doubles):
  	if is_doubles:
      if i % 2 == 0:
        del(team)
        team = Team()
        team.add_teammate(player)
      else:
        team.add_teammate(player)
        slots.append(team)
      i += 1

    if not is_doubles:
      del(team)
      team = Team()
      team.add_teammate(player)
      slots.append(team)

  def __get_number_of_players_and_slots_tuple(self, player_list, is_doubles):
    number_of_players = len(player_list)
    number_of_slots = number_of_players
    if is_doubles:
      number_of_slots = number_of_players / 2

    return number_of_players, number_of_slots


  def reset(self, handle):
    '''
    Reset the users match.
    '''
    response = ""
    user_id = self.__user_ids[handle]
    player = self.__players[user_id]
    winner_games = self.__winners.get_games()
    match = winner_games[player.get_match_id()]
    response = match.reset_game(user)

    if response == "":
      response = "Player not found in tournament."

    return response

  def next(self):
    '''
    Advance the bracket to the next round if all the games are complete.
    '''
    response = ""
    if self.is_complete():
      response = self.__winners.advance()
    else:
      response = "The matches are not all complete."

    return response

  def help(self, key):
    # call the readmedocs app
    pass

  def win(self, user):
    '''
    Report a win if the game is not already complete and also
    check for a champion.
    '''
    games = self.__winners.get_games()
    if len(games) == 0:
      return "The tournament has not started."

    if user == None or user not in self.__players:
      return "Player not found in tournament."

    response = ""
    player = self.__players[user]
    match_id = player.get_match_id()
    if match_id != None:
      match = games[match_id]
      response = match.add_win(user)
    else:
      response = "Player is not in the tournament."

    return response

  def loss(self, user):
    '''
    Report a loss if the game is not already complete 
    '''
  
    games = self.__winners.get_games()
    if len(games) == 0:
      return "The tournament has not started."

    if user == None or user not in self.__players:
      return "Player not found in tournament."

    response = ""
    player = self.__players[user]
    match_id = player.get_match_id()
    if match_id != None:
      match = games[match_id]
      response = match.add_loss(user)
    else:
      response = "Player is not in the tournament."

    return response

  def clear(self):
    self.__players.clear()
    return "Players have been cleared."

  def destroy(self):
    self.__bracket.destroy()
    return "Games have been destroyed"

  def __get_order_preset(self, presets):
    '''
    Flip everyother postion in the list to feed it to tree generator.
    '''
    response = presets
    size = len(response)

    i = 0
    j = 1
    while j < size:
      response[i], response[j] = response[j], response[i]
      i += 2
      j += 2

    response.reverse()
    return response

  def get_printed(self):
    '''
    Loop through the list and print each game.
    '''
    games = self.__winners.get_games()

    string = ""
    number_of_games = len(games)
    if number_of_games == 0:
      return "The tournament has not started."
    
    champion = False
    if number_of_games == 1 and self.is_complete():
      champion = True 

    i = 1
    champ = ""
    for match in games:
      if champion:
        winner = match.get_winner()
        name = winner.get_name()
        if name == "":
          name = winner.get_handle()
        if self.__is_doubles:
          champ = "\n" + name + " are the tournament champions!\n"
        else:
          champ = "\n" + name + " is the tournament champion!\n"
        champ += "Grand Prize: :tada: :trophy: :cookie:\n"
      if number_of_games == 1:
        string = "%s\n*Championship Match*: \n" % (string)
      else:
        string = "%s\n*Match: %d*\n" % (string, i)
      string = "%s%s\n" % (string, match.get_score())
      i += 1
    
    return champ + string

  def is_complete(self):
    '''
    Check if all the matches in the current round are complete.
    '''
    response = True
    games = self.__winners.get_games()
    if len(games) == 0:
      response = False
    else:
      for match in games:
        if match.is_complete() == False:
          response = False

    return response

  def is_in_progress(self):
    return len(self.__winners.get_games()) > 0

  def get_user_id(self, handle):
    return self.__user_ids[handle]