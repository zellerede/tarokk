from collections import deque

import myDict
myDict.addTo(globals())

from util import *
addSymbolsTo(globals())


#######################################
#
class Card(object):
#######################################
  colors = Symbols('TAROKK',_CLUBS,_DIAMONDS,_SPADES,_HEARTS, start=0)
  figures = Symbols(_ACE,_JACK,_KNIGHT,_QUEEN,_KING)
  tarocks = Symbols('I','II','III','IIII','V','VI','VII','VIII','IX','X',
                    'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII',
                    'XIX','XX','XXI','SKIZ') # 'SKIZ' = _CLOWN, but referred
  honours = set()
  kings   = set()
  
  _createdCards = {}
  # singletoning
  def __new__(cls, num, color=TAROKK):
    if (color,num) in Card._createdCards:
      return Card._createdCards[(color,num)]
    newCard = object.__new__(cls, num, color)
    Card._createdCards[(color,num)] = newCard
    return newCard
  
  def __init__(self, num, color=TAROKK):
    self.color = color
    self.num = num
    self.isTarock = (color==TAROKK)
    if self.isTarock:
      if num in [I,XXI,SKIZ]: 
        self.value = 5
        Card.honours.add(self)
      else: 
        self.value = 1
    else:
      self.value = num.index
      if self.value==5: # king
        Card.kings.add(self)
  
  def __repr__(me):
    if me.isTarock: return str(me.num)
    else: 
      # for HUN
      # return "%s %s" %(me.color, me.num)
      # for ENG
      return "%s OF %s" %(me.num, me.color)
  
  def __gt__(me, other):
    if not other: return True
    if (me.color != other.color):
      return me.isTarock
    return me.num > other.num

#######################################
#
class Deck(deque):
#######################################
  def __init__(self, arg=None):
    if arg:
      deque.__init__(self, arg)
      return
    for color in Card.colors:
      if color==TAROKK:
        for tarock in Card.tarocks:
          self.append(Card(tarock))
      else:
        for figure in Card.figures:
          self.append(Card(figure, color))
  def __repr__(self):
    return "Deck%s" % self
  def __str__(self):
    return "["+ ", ".join([str(x) for x in self]) +"]"
  
  def deal(self, numOfCards):
    cards = []
    for i in range(numOfCards):
      cards.append(self.popleft())
    return Deck(cards)

# Precreate all cards:
Deck()
