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
from match import MATCH_STATUS_COMPLETE
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
    self.__bracket.destroy()
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
      response = "Singles bracket generated from presets."

    self.__bracket.generate(slots, is_random)

    return response

  def doubles(self, user, presets):
    self.__bracket.destroy()
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

    if is_odd:
      if is_preset:
        return "There is an odd number of presets."
      else:
        # remove the send from the players list if the count is odd
        del self.__players[user]

    response = ""
    team = None
    slots = []
    is_random = len(presets) == 0
    i = 0
    if is_random:
      for key in self.__players:
        rand_int = random.choice(range(number_of_players))
        random_player = self.__players[rand_int]
        del self.__players[rand_int]
        
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
        match.reset_game(user)

        if self.__is_doubles:
          response = "Match has been reset."
        else:
          response = player.get_name() + "'s match has been reset"

    if response == "":
      response = "Player not found in tournament."

    return response

  def boot(self, handle):
    '''
    Disqualify the user with the handle provided and give the win to the opponent.
    '''
    response = ""
    for key in self.__players:
      player = self.__players[key]
      if handle == player.get_handle():
        games = self.__bracket.get_games()

        user = player.get_user()
        player = self.__players[user]
        match = games[player.get_match_id()]
        match.quit_player(user)

        if self.__is_doubles:
          response = "Player has been disqualified."
        else:
          response = player.get_name() + " has been disqualified."

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
      return "The game was not found."

    if user not in self.__players:
      return "Player not found in tournament."
    
    player = self.__players[user]
    match = games[player.get_match_id()]
    match.add_win(user)

    response = ""
    if match.match_status() == MATCH_STATUS_COMPLETE:
      response = "The match was won by " + match.get_winner().get_name()
    else:
      response = player.get_name() + " repoted a win."

    return response

  def clear(self):
    self.__players.clear()
    return "Players have been cleared."

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
        if self.__is_doubles:
          champ = match.get_winner().get_name() + " are the tournament champions!\n"
        else:
          champ = match.get_winner().get_name() + " is the tournament champion!\n"
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
