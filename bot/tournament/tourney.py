#!/usr/bin/python

# Created by: JRG
# Date: Aug 31, 2016
#
# Description: The tournament object will allow the slack bot to create a
# tournament with the users in the channel. It also provides methods to
# prgress the tournament and eventually crown a winner.

from player import Player
from team import PlayerTeam
from match import Match
from tree import TourneyTree
from participants import Participants
from presets import Presets
import random

class Tourney:
  '''
  This class provides methods to manage the tournament tree bracket.
  '''

  def __init__(self):
    self.__channel_users = {}
    self.__user_ids = {}
    self.__bracket = TourneyTree()
    self.__last_post = None
    self.participants = Participants()
    self.presets = Presets()
    self.is_joinable = False

  def set_last_post(self, last_post):
    self.__last_post = last_post
 
  def get_last_post(self):
    return self.__last_post
  
  def add_channel_user(self, player):
    self.__channel_users[player.get_user()] = player
    self.__user_ids[player.get_handle()] = player.get_user()

  # def remove_channel_user(self, player_id):
  #   player = self.__channel_users[player_id]
  #   user_id = player.get_user()
  #   handle =player.get_handle()

  #   del self.__channel_users[user_id]
  #   del self.__user_ids[handle]
       
  def singles(self):
    self.__last_post = None

    number_of_slots = 0
    number_of_presets = len(self.presets.get_all())
    is_random = number_of_presets == 0
    if is_random:
      if self.is_joinable:
        number_of_slots = len(self.participants.get_handles())
      else:
        number_of_slots = len(self.__channel_users)
    else:
      number_of_slots = number_of_presets

    if number_of_slots < 2:
      return "There are not enough players."

    response = ""
    team = None
    slots = []
    if is_random:
      users = {}
      if self.is_joinable:
        for participant in self.participants.get_handles():
          user_id = self.__user_ids[participant]
          users[user_id] = participant
      else:
        users = self.__channel_users

      for key in users:
        del(team)
        team = PlayerTeam()
        team.add_player(self.__channel_users[key])
        slots.append(team)
      response = "Singles bracket randomly generated."
    else:
      for handle in self.presets.get_all():
        if handle == "-bye-":
          del(team)
          team = PlayerTeam()
          slots.append(team)
        else:
          del(team)
          team = PlayerTeam()

          user_id = self.__user_ids[handle]
          player = self.__channel_users[user_id]
          team.add_player(player)

          slots.append(team)

      slots = self.__get_order_preset(slots)
      response = "Singles bracket generated from presets."

    self.__bracket.generate(slots, is_random)

    return response

  def doubles(self, user):
    self.__last_post = None
    
    number_of_slots = 0
    number_of_presets = len(self.presets.get_all())
    is_random = number_of_presets == 0
    if is_random:
      number_of_players = len(self.__channel_users)
      number_of_slots = number_of_players / 2
    else:
      number_of_players = number_of_presets
      number_of_slots = number_of_players / 2
      
    is_odd = number_of_players % 2 == 1    
    
    if number_of_slots < 2:
      return "There are not enough players."

    if is_odd and is_preset:
      return "There is an odd number of presets."

    response = ""
    team = None
    slots = []
    i = 0
    if is_random:
      players = []
      if self.is_joinable:
        users = {}
        for participant in self.participants.get_handles():
          user_id = self.__user_ids[participant]
          users[user_id] = participant
        for key in users:
          if not is_odd or key != user:
            players.append(self.__channel_users[key]) 
      else:
        for key in self.__channel_users:
          if not is_odd or key != user:
            players.append(self.__channel_users[key]) 

      for x in range(len(players)):
        rand_int = random.choice(range(len(players)))
        random_player = players[rand_int]
        del players[rand_int]
        
        if i % 2 == 0:
          del(team)
          team = PlayerTeam()
          team.add_player(random_player)
        else:
          team.add_player(random_player)
          slots.append(team)
        i += 1

      response = "Doubles bracket randomly generated."
    else:
      for handle in self.presets.get_all():
        user_id = self.__user_ids[handle]
        player = self.__channel_users[user_id]
        if handle == "-bye-":
          del(team)
          team = PlayerTeam()
          slots.append(team)
        elif player.get_handle() == handle:
          if i % 2 == 0:
            del(team)
            team = PlayerTeam()
            team.add_player(player)
          else:
            team.add_player(player)
            slots.append(team)
          i += 1

      slots = self.__get_order_preset(slots)
      response = "Doubles bracket generated from presets."
    
    self.__bracket.generate(slots, is_random)

    return response

  def reset(self, handle):
    '''
    
    '''
    response = ""
    if handle in self.__user_ids:
      user_id = self.__user_ids[handle]
      player = self.__channel_users[user_id]
      games = self.__bracket.get_round_matches()
      match = games[player.get_match_id()]
      response = match.reset_game(user_id)

    if response == "":
      response = "Player not found in tournament."

    return response

  def next(self):
    '''
    Advance the bracket to the next round if all the games are complete.
    '''
    response = ""
    games = self.__bracket.get_round_matches()
    if len(games) == 0:
      response = "The tournament has not started."
    elif self.is_round_complete():
      self.__last_post = None
      response = self.__bracket.advance()
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
    games = self.__bracket.get_round_matches()
    if len(games) == 0:
      return "The tournament has not started."

    if user == None or user not in self.__channel_users:
      return "Player not found in tournament."

    response = ""
    player = self.__channel_users[user]
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
  
    games = self.__bracket.get_round_matches()
    if len(games) == 0:
      return "The tournament has not started."

    if user == None or user not in self.__channel_users:
      return "Player not found in tournament."

    response = ""
    player = self.__channel_users[user]
    match_id = player.get_match_id()
    if match_id != None:
      match = games[match_id]
      response = match.add_loss(user)
    else:
      response = "Player is not in the tournament."

    return response

  def clear_users(self):
    self.__channel_users.clear()
    self.__user_ids.clear()
    return "Players have been cleared."

  def destroy(self):
    self.clear_users()
    self.__bracket.destroy()
    self.__last_post = None
    self.participants.clear_users()
    self.presets.clear_users()
    self.is_joinable = False
    
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
    games = self.__bracket.get_round_matches()

    string = ""
    number_of_games = len(games)
    if number_of_games == 0:
      return "The tournament has not started."
    
    champion = False
    if number_of_games == 1 and self.is_round_complete():
      champion = True 

    i = 1
    champ = ""
    for match in games:
      if champion:
        winner = match.get_winner()
        name = winner.get_name()
        if name == "":
          name = winner.get_handle()
        if winner.is_single_player():
          champ = "\n" + name + " is the tournament champion!\n"
        else:
          champ = "\n" + name + " are the tournament champions!\n"
        champ += "Grand Prize: :tada: :trophy: :cookie:\n"
      if number_of_games == 1:
        string = "%s\n*Championship Match*: \n" % (string)
      else:
        string = "%s\n*Match: %d*\n" % (string, i)
      string = "%s%s\n" % (string, match.get_score())
      i += 1
    
    return champ + string

  def is_round_complete(self):
    '''
    Check if all the matches in the current round are complete.
    '''
    response = True
    games = self.__bracket.get_round_matches()
    for match in games:
      if match.is_complete() == False:
        response = False

    return response

  def add_participant(self, user_id):
    response = ""
    if user_id in self.__channel_users:
      player = self.__channel_users[user_id]
      response = self.participants.add_user(player.get_handle(), self.get_channel_users())
    else:
      response = "Player not found."

    return response

  def list_players(self):
    number_of_players = self.participants.get_count()
    response = "\n*Registered Players ({})*:\n".format(number_of_players)
    if number_of_players == 0:
      response += "None"
    
    for handle in self.participants.get_handles():
      user_id = self.__user_ids[handle]
      player = self.__channel_users[user_id]
      response += player.get_handle_and_name() + "\n"

    return response

  def get_user(self, user_id):
    response = None
    user_upper = user_id.upper()
    if user_upper in self.__channel_users:
      response = self.__channel_users[user_upper]

    return response

  def get_user_id(self, handle):
    response = None
    if handle in self.__user_ids:
      response = self.__user_ids[handle]
      
    return response

  def get_channel_users(self):
    users = []
    for user_id in self.__channel_users:
      users.append(self.__channel_users[user_id])

    return users

  # To-Do: May not need this after creating messanger app, can get matches from db
  def get_round_matches(self):
    return self.__bracket.get_round_matches()


def main():
  tourney = Tourney()
  tourney.add(Player("U123", "abc", "fabc", "labc"))
  tourney.add(Player("U456", "def", "fdef", "ldef"))

  tourney.singles([])
  print ""
  
  print tourney.get_printed()
  print ""

  tourney.win("U123")
  print ""

  print tourney.get_printed()

if __name__ == '__main__':
  main()
