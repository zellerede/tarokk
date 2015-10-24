'''Tarokk'''

from random import randint, shuffle
from collections import deque

#######################################
#
#  utility stuff: 
#   - Symbols, 
#   - processing a sequence of tasks
#
#######################################

class Symbol(object):
  def __init__(self, name, idx):
    self.name = name
    self.index = idx
  def __repr__(self):
    return "(symbol)%s" % self.name
  def __str__(self):
    return self.name

def Symbols(*symbols,**instructions):
  idx = instructions.get('start', 1)
  symGroup = {}
  for sym in symbols:
    globals()[sym] = symGroup[idx] = Symbol(sym, idx)
    idx += 1
  return symGroup

#######################################

def process(*funcs):
  for f in funcs:
    print "Processing", f.__name__
    f()


#######################################
#
class Card(object):
#######################################
  colors = Symbols('TAROKK','TREFF','KARO','PIKK','KOR', start=0)
  figures = Symbols('ASZ','BOTOS','LOVAS','DAMA','KIRALY')
  tarocks = Symbols('I','II','III','IIII','V','VI','VII','VIII','IX','X',
                    'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII',
                    'XIX','XX','XXI','SKIZ')              
  
  def __init__(my, num, color=TAROKK):
    my.color = color
    my.num = num
    my.isTarock = (color==TAROKK)
    my.isHonour = False
    if my.isTarock:
      if num in [I,XXI,SKIZ]: 
        my.value = 5
        my.isHonour = True
      else: 
        my.value = 1
    else:
      my.value = num.index
  
  def __repr__(me):
    if me.isTarock: return str(me.num)
    else: return "%s %s" %(me.color, me.num)
  
  def __gt__(me, other):
    if not other: return True
    return me.num > other.num
  
  @staticmethod
  def random():
    # to randomize -- would we ever need it?
    return Card(KIRALY, PIKK)

#######################################
#
class Deck(deque):
#######################################
  def __init__(self, arg=None):
    if arg:
      deque.__init__(self, arg)
      return
    for color in Card.colors.values():
      if color==TAROKK:
        for tarock in Card.tarocks.values():
          self.append(Card(tarock))
      else:
        for figure in Card.figures.values():
          self.append(Card(figure, color))
  def __repr__(self):
    return "Deck%s" % self
  def __str__(self):
    return "["+ ", ".join([str(x) for x in self]) +"]"
  
  def deal(self, numOfCards):
    cards = []
    for i in range(numOfCards):
      cards.append(self.popleft())
    return cards

#######################################
#
class Table(object):
#######################################
  def __init__(self):
    self.deck = Deck()
    self.players = [UserPlayer('Eszak'), AIPlayer('Nyugat'), AIPlayer('Del'), AIPlayer('Kelet')]
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
  # phases = Symbols('KEVER', 'EMEL', 'OSZT', 'LICIT', 'SKART', 'BEMOND', 'LEJATSZ', 'FIZET')
  
  def __init__(Q, table):
    Q.table = table
    Q.caller = (table.dealer+1) % 4
    process(Q.kever, Q.emel, Q.oszt, Q.licit, Q.skart, Q.bemond, Q.lejatsz, Q.fizet)
  
  def kever(self):
    n = randint(1,8)
    for i in range(n):
      shuffle(self.table.deck)
    # debug
    print self.table.deck
  
  def emel(self):
    em = self.table.players[self.table.dealer -1].emel()
    self.table.deck.rotate(em)
    # debug
    print self.table.deck
  
  def oszt(self):
    # 6 talon
    self.talon = self.table.deck.deal(6)
    self._ossz(5)
    self._ossz(4)
    # debug
    print self.table.deck
    print self.talon
 
  def _ossz(self, n):
    for i in range(self.caller, self.caller +4):
      j = i%4
      self.table.players[j].cards += self.table.deck.deal(n)
  
  def licit(self):
    pass
    
  def skart(self):
    pass
  
  def bemond(self):
    pass
  
  def lejatsz(self):
    n = len(self.table.players[0].cards)
    hit = None
    winner = -1
    for i in range(n):
      Round=[]
      for j in range(self.caller, self.caller+4):
        k = j%4
        card = self.table.players[k].call(Round)
        Round.append(card)
        if card > hit: 
          hit = card
          winner = k
      self.caller = winner
      self.table.players[winner].take(Round)
      print self.table.players[winner].name, Round
    
  def fizet(self):
    pass

  _phases = [kever, emel, oszt, licit, skart, bemond, lejatsz, fizet]

class Player(object):
  def __init__(self, name):
    self.name = name
    self.cards = []
    self.hits = []
  def take(self, hits):
    self.hits += hits


class AIPlayer(Player):
  def emel(self):
    return randint(1,39)
  def call(self, sofar):
    return self.cards.pop(randint(0,len(self.cards)-1))

class UserPlayer(Player):
  def emel(self):
    return 42 - int( raw_input("Hol emeled el? [2--40] ") )
  def call(self, sofar):
    return self.cards.pop(randint(0,len(self.cards)-1))

#######################################
#
if __name__ == '__main__':
#######################################
  table = Table()
  table.newParty()
