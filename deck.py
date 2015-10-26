from collections import deque

execfile("util.py")
#from util import *

_createdCards = {}

#######################################
#
class Card(object):
#######################################
  colors = Symbols('TAROKK','TREFF','KARO','PIKK','KOR', start=0)
  figures = Symbols('ASZ','BOTOS','LOVAS','DAMA','KIRALY')
  tarocks = Symbols('I','II','III','IIII','V','VI','VII','VIII','IX','X',
                    'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII',
                    'XIX','XX','XXI','SKIZ')              
  
  # singleton
  def __new__(cls, num, color=TAROKK):
    global _createdCards
    
    if (color,num) in _createdCards:
      return _createdCards[(color,num)]
    newCard = object.__new__(cls, num, color)
    _createdCards[(color,num)] = newCard
    return newCard
  
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
    if (me.color != other.color):
      return me.isTarock
    return me.num.index > other.num.index

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
    return Deck(cards)
