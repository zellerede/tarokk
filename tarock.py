'''Tarokk'''

from random import randint, shuffle

from util import *
from deck import *
from players import *

#######################################
#
class Table(object):
#######################################
  def __new__(cls, table=None):
    if table: return table
    return object.__new__(cls)
    
  def __init__(self, table=None):
    if table: return   # should not be the case
    self.deck = Deck()
    self.players = Players( 
         [UserPlayer('Eszak'), AIPlayer('Nyugat'), AIPlayer('Del'), AIPlayer('Kelet')] )
    self.dealer = -1 # so that user will start
    self.base = 1 # one unit of money
    # etc.
 
  def newParty(self):
    Party(self)
    self.dealer += 1
    while self.dealer >= len(self.players):
      self.dealer -= len(self.players)

#######################################
#
class Party(object):
#######################################
  # todo: Party(Table) and inherit all properties at __new__/__init__ instead of copying them...
  
  def __init__(Q, table):
    Q.table = table
    Q.caller = (table.dealer+1) % len(table.players)
    for player in table.players.allFrom(Q.caller):
      player.newHand()
    process(Q.kever, Q.emel, Q.oszt, Q.licit, Q.skart, Q.bemond, Q.lejatsz, Q.fizet)
  
  def kever(self):
    n = randint(1,8)
    for i in range(n):
      shuffle(self.table.deck)
    # debug
    # print self.table.deck
  
  def emel(self):
    emelo = self.table.players[self.table.dealer -1]
    em = 42 - emelo.emel()
    self.table.deck.rotate(em)
    # debug
    # print self.table.deck
  
  def oszt(self):
    # 6 talon
    self.talon = self.table.deck.deal(6)
    self._ossz(5)
    self._ossz(4)
    for player in self.table.players.allFrom():
      player.showCards()

  def licit(self):
    self.teller = self.caller
    
  def skart(self):
    self.skart = self.talon[:]
  
  def bemond(self):
    partnerCard = self.table.players[self.teller].askPartner()
    # debug
    print self.table.players[self.teller], "will be with who has", partnerCard
    self._arrangeGrpWithWhoHas(partnerCard)
    # further figures to make
  
  def lejatsz(self):
    n = len(self.table.players[0].cards)
    for i in range(n):
      hit = None
      winner = -1
      Round=[]
      for j in self.table.players.indicesFrom(self.caller):
        card = self.table.players[j].call(Round)
        Round.append(card)
        if card > hit: 
          hit = card
          winner = j
      self.caller = winner
      self.table.players[winner].take(Round)
      print self.table.players[winner].name, hit, ':', Round
    
  def fizet(self):
    print
    print "Felvevok:", self.challengers
    summ=0
    for p in self.challengers:
      s = sum([h.value for h in p.hits])
      print p, "vitt:", s
      summ += s
    print "Szumma", summ, "pont"
    print "-"*32
    summ=0
    for p in self.poors:
      s = sum([h.value for h in p.hits])
      print p, "vitt:", s
      summ += s
    print "Szumma", summ, "pont"
    
    for p in self.table.players:
      self.table.deck += p.hits
    self.table.deck += self.skart
    
    # talon
    print "Skart volt:", self.skart

##############################
#
  def _arrangeGrpWithWhoHas(self, card):
    partner = None
    allPlayers = set( self.table.players.all() )
    for player in allPlayers:
      if card in player.cards:
        partner = player
    self.challengers = {self.table.players[self.teller]}
    if partner:
      self.challengers.add( partner )
    self.poors = allPlayers - self.challengers
  
  
  def _ossz(self, n):
    for player in self.table.players.allFrom(self.caller):
      player.cards += self.table.deck.deal(n)
  


###
# dev
def clean():
  import sys
  del sys.modules['util']
  del sys.modules['deck']
  del sys.modules['players']

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
  table.newParty()

