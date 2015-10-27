'''Tarokk'''

from random import randint, shuffle

from util import *
from deck import *
from players import *
from scenarios import *

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
         [UserPlayer('Eszak'), AIPlayer('Nyugat'), AIPlayer('Del'), AIPlayer('Kelet')] )
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
    # print self.deck
  
  def emel(self):
  #######################################
    emelo = self.players[self.dealer -1]
    em = 42 - emelo.emel()
    self.deck.rotate(em)
    # debug
    # print self.deck
  
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
    print self.players[self.teller], "nyeri a licitet: ***", self.numOfCardsToChange, "***"
    self.partyPay = 4 - self.numOfCardsToChange
    # self.scenarios[PARTY].pay = 4 - self.numOfCardsToChange
    
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
    print self.players[self.teller], "will be with who has", partnerCard
    self._arrangeGrpWithWhoHas(partnerCard)
    # further figures to make
  
  def lejatsz(self):
  #######################################
    n = len(self.players[self.caller].cards)
    for i in range(n):
      hit = None
      winner = -1
      Round=[]
      for j in self.players.indicesFrom(self.caller):
        card = self.players[j].call(Round)
        Round.append(card)
        if card > hit: 
          hit = card
          winner = j
      self.caller = winner
      self.players[winner].take(Round)
      print self.players[winner].name, hit, ':', Round
    
  def fizet(self):
  #######################################
    print
    print "Felvevok:", self.challengers
    self._collectHitsOf(self.challengers)
    self._collectHitsOf(self.poors) # todo: arrange skart as well
    
    self.poors.hits += self.skartolt
    
    for scenario in self.scenarios:
      scenario.getWinner()

    # collect back the deck    
    for team in self.teams:
      self.deck += team.hits

    # skart
    print "Ellenfel skartja volt:", self.skartolt
    print "\n"+ '-'*42 +"\n"

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
  
  def _collectHitsOf(self, team):
    allHits = []
    for player in team:
      allHits += player.hits
    team.hits = allHits
  
  def _ossz(self, n):
    for player in self.players.allFrom(self.caller):
      player.cards += self.deck.deal(n)


###
# dev
def clean():
  import sys
  del sys.modules['util']
  del sys.modules['deck']
  del sys.modules['players']
  del sys.modules['scenarios']

def auto(on=True):
  if on:
    table.players[0] = AIPlayer('Eszak')
  else:
    table.players[0] = UserPlayer('Eszak')

#######################################
#
if __name__ == '__main__':
#######################################
  table = Table()
  auto()
  # while True:
  table.newParty()
