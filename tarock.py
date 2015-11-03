'''Tarokk'''

from random import randint, shuffle

from util import *
from deck import *
from players import *
from scenarios import *
import textItems
textItems.addTo(globals()) # get all string literals as global variables

CHANGE_SEQUENCE = [ (0,2,2,2),
                    (1,2,2,1),
                    (2,2,1,1),
                    (3,1,1,1) ]

#######################################
#
class Table(object):
#######################################
  def __init__(self):
    self.deck = Deck()
    self.players = Players( 
         [UserPlayer(_North), AIPlayer(_West), AIPlayer(_South), AIPlayer(_East)] )
    self.dealer = -1 # so that user will start
    self.base = 1 # one unit of money
    # etc.
 
  def newParty(self):
    Party(self) # the Party instance overlaps all attributes of self
    self.dealer += 1
    self.dealer %= len(self.players)

#######################################
#
@buildOnObject
class Party(object):
#######################################
  
  def __init__(self): 
  # we will have an addition Table type parameter with shared attributes(!!!)
    self.caller = (self.dealer+1) % len(self.players)
    for player in self.players.allFrom(self.caller):
      player.newHand()
    self.scenarios = [scena(self) for scena in SCENARIOS]
    process(self.kever, 
            self.emel, 
            self.oszt, 
            self.licit, 
            self.skart, 
            self.bemond, 
            self.lejatsz, 
            self.fizet)
 
 
  def kever(self):
  ####################################### 
    n = randint(1,8)
    for i in range(n):
      shuffle(self.deck)
    # debug
    # display(self.deck)
  
  def emel(self):
  #######################################
    emelo = self.players[self.dealer -1]
    em = 42 - emelo.emel()
    self.deck.rotate(em)
    # debug
    # display(self.deck)
  
  def oszt(self):
  #######################################
    # 6 talon
    self.talon = self.deck.deal(6)
    self._ossz(5)
    self._ossz(4)
    for player in self.players.all():
      player.showCards()

  def licit(self):
  #######################################
    self.teller = self.caller
    self.numOfCardsToChange = self.players[self.teller].licit()
    display(self.players[self.teller], _wins_the_bidding_____, self.numOfCardsToChange, "***")
    self.partyPay = 4 - self.numOfCardsToChange
    # self.scenarios[Parti].pay = 4 - self.numOfCardsToChange
    
  def skart(self):
  #######################################
    self.skartolt = []
    i = 0
    changeSequence = CHANGE_SEQUENCE[self.numOfCardsToChange]
    for player in self.players.allFrom(self.teller):
      num = changeSequence[i]
      if num:
        newCards = self.talon.deal( num )
        player.cards += newCards
        player.showCards()
        fektetett = player.fektet( num )
        if i: 
          self.skartolt += fektetett
        else:
          player.hits += fektetett
      i += 1
  
  def bemond(self):
  #######################################
    partnerCard = self.players[self.teller].askPartner()
    # debug
    display(self.players[self.teller], "will be with who has", partnerCard)
    self._arrangeGrpWithWhoHas(partnerCard)
    # further figures to make
    self.promised = [Parti]
  
  def lejatsz(self):
  #######################################
    n = len(self.players[self.caller].cards)
    self.rounds = []
    for i in range(n):
      hit = None
      winner = -1
      rundo = Round(caller=self.caller)
      for j in self.players.indicesFrom(self.caller):
        card = self.players[j].call(rundo)
        rundo.append(card)
        if card > hit: 
          hit = card
          winner = j
      rundo.winner = winner
      rundo.winnerCard = hit
      self.rounds.append(rundo)
      self.caller = winner
      self.players[winner].take(rundo)
      display(self.players[winner].name, hit, ':', rundo)
    
  def fizet(self):
  #######################################
    display()
    display(_Declarers_, self.challengers)
    self._collectHitsOf(self.challengers)
    self._collectHitsOf(self.poors) # todo: arrange skart as well
    
    self.poors.hits += self.skartolt
    
    for scenario in self.scenarios:
      scenario.investigate()
    
    for player in self.players.all():
      display(player, ":", player.cash, " \t",)
    display()
    display('-'*84)
    display()

    # collect back the deck    
    for team in self.teams:
      self.deck += team.hits

    # skart
    display(_Discards_of_opponent_were_, self.skartolt)
    display("\n"+ '-'*42 +"\n")

##############################
#
  def _arrangeGrpWithWhoHas(self, card):
    partner = None
    allPlayers = Players( self.players.all() )
    for player in allPlayers:
      if card in player.cards:
        partner = player
    self.challengers = Players([ self.players[self.teller] ])
    if partner:
      self.challengers.append( partner )
    self.poors = allPlayers - self.challengers
    self.teams = (self.challengers, self.poors)
 
  def teamOf(self, player):
    if not isinstance(player, Player):
      player = self.players[player]
    for team in self.teams:
      if player in team: return team
  
  def otherTeam(self, team):
    i = self.teams.index(team)
    return self.teams[1-i]
  
  def _collectHitsOf(self, team):
    allHits = []
    for player in team:
      allHits += player.hits
    team.hits = allHits
  
  def _ossz(self, n):
    for player in self.players.allFrom(self.caller):
      player.cards += self.deck.deal(n)

##############################
#
class Round(list):
##############################
  def __init__(self, *args, **kws):
    list.__init__(self, *args)
    for attr in kws:
      setattr(self, attr, kws[attr])

  def whoHad(self, card):
    if card not in self: 
      return
    return (self.index(card) + self.caller)


################################################################
###
##   ...dev
#
#
def clean():
  import sys
  del sys.modules['util']
  del sys.modules['deck']
  del sys.modules['players']
  del sys.modules['scenarios']
  del sys.modules['textItems']

def auto(on=True):
  cash = table.players[0].cash
  if on:
    me = table.players[0] = AIPlayer(_North)
    me.cash = cash
  else:
    me = table.players[0] = UserPlayer(_North)
    me.cash = cash

class WithoutParenthesis:
  def __init__(self, noArgFunc):
    self.func = noArgFunc
  def __repr__(self):
    self.func()
    return ''

def Without():
  return WithoutParenthesis

@Without()
def n():
  if len(table.deck)!=42:
    table.deck = Deck()
  table.newParty()


#######################################
#
if __name__ == '__main__':
#######################################
  table = Table()
  # auto()
  goOn = True
  while goOn:
    table.newParty()
    more = my_input(_Play_more__)
    goOn = not more.upper().startswith('N')
