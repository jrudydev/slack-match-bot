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
from tree import TournyTree
import random

class Tourny:
  '''
  This class provides methods to manage the tournament tree bracket.
  '''

  def __init__(self):
    self.__players = {}
    self.__bracket = TournyTree()
    self.__is_doubles = False
  
  def add(self, player):
    self.__players[player.get_user()] = player
       
  def singles(self, presets):
    self.__is_doubles = False

    number_of_slots = 0
    if len(presets) > 0:
      number_of_slots = len(presets)
    else:
      number_of_slots = len(self.__players)

    if number_of_slots < 2:
      return "There are not enough players."

    response = ""
    slots = []
    is_random = len(presets) == 0
    if is_random:
      for key in self.__players:
        slots.append(self.__players[key])
      response = "Singles bracket randomly generated."
    else:
      for handle in presets:
        for key in self.__players:
          player = self.__players[key]
          if player.get_handle() == handle:
            slots.append(player)
            break

      slots = self.__get_oreder_preset(slots)
      response = "Singles bracket generated from presets."

    self.__bracket.generate(slots, is_random)

    return response

  def doubles(self, user, presets):
    self.__is_doubles = True
    
    number_of_slots = 0
    is_preset = len(presets) > 0
    if is_preset:
      number_of_players = len(presets)
      number_of_slots = number_of_players / 2
    else:
      number_of_players = len(self.__players)
      number_of_slots = number_of_players / 2
    is_odd = number_of_players % 2 == 1    
    
    if number_of_slots < 2:
      return "There are not enough players."

    if is_odd and is_preset:
      return "There is an odd number of presets."

    response = ""
    team = None
    slots = []
    is_random = len(presets) == 0
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
        
        if i % 2 == 0:
          del(team)
          team = Team()
          team.add_teammate(random_player)
        else:
          team.add_teammate(random_player)
          slots.append(team)
        i += 1

      response = "Doubles bracket randomly generated."
    else:
      for handle in presets:
        for key in self.__players:
          player = self.__players[key]
          if player.get_handle() == handle:
            if i % 2 == 0:
              del(team)
              team = Team()
              team.add_teammate(player)
            else:
              team.add_teammate(player)
              slots.append(team)
            i += 1
            break

      slots = self.__get_oreder_preset(slots)
      response = "Doubles bracket generated from presets."
    
    self.__bracket.generate(slots, is_random)

    return response

  def reset(self, handle):
    '''
    
    '''
    response = ""
    for key in self.__players:
      player = self.__players[key]
      if handle == player.get_handle():
        games = self.__bracket.get_games()

        user = player.get_user()
        player = self.__players[user]
        match = games[player.get_match_id()]
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
    games = self.__bracket.get_games()
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
  
    games = self.__bracket.get_games()
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

  def __get_oreder_preset(self, presets):
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
    games = self.__bracket.get_games()

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
    games = self.__bracket.get_games()
    if len(games) == 0:
      response = False
    else:
      for match in games:
        if match.is_complete() == False:
          response = False

    return response

  def is_in_progress(self):
    return len(self.__bracket.get_games()) > 0

  def get_user_id(self, handle):
    response = None
    for key in self.__players:
      if self.__players[key].get_handle() == handle:
        response = key
        break

    return response


def main():
  tourny = Tourny()
  tourny.add(Player("U123", "abc", "fabc", "labc"))
  tourny.add(Player("U456", "def", "fdef", "ldef"))

  tourny.start()
  print ""
  
  print tourny.get_printed()
  print ""

  tourny.win("U123")
  print ""

  print tourny.get_printed()

if __name__ == '__main__':
  main()
