from random import randint, choice

from deck import *
from util import my_input

class Players(list):
  def allFrom(self, idx=0):
    for i in self.indicesFrom(idx):
      yield self[i]
  
  def indicesFrom(self, idx=0):
    for i in range(idx, idx+4):
      yield i % len(self)
    

#######################################
#
class Player(object):
#######################################
  def __init__(self, name):
    self.name = name
    self.newHand()
  def newHand(self):
    self.cards = []
    self.hits = []
  def take(self, hits):
    self.hits += hits
  def __repr__(self):
    return "Player %s" % self.name
  def __str__(self):
    return str(self.name)
  
  def showCards(self):
    pass
  
  def cardsOfColor(self, color):
    return [card for card in self.cards if card.color==color]
    
  def has(self, color):
    return bool( self.cardsOfColor(color) )
  
  def anyCard(self, color=None):
    cardsToCall = self.cardsOfColor(color)
    if not cardsToCall:
      cardsToCall = self.cards[:]
    return choice(cardsToCall)

  def select(self, sofar):
    if not sofar:
      return self.anyCard()
    color = sofar[0].color
    if not self.has(color):
      color = TAROKK
    return self.anyCard(color)
  
  def call(self, sofar):
    card = self.select( sofar )
    self.cards.remove(card)
    return card

#######################################
#
class AIPlayer(Player):
#######################################
  def emel(self):
    return randint(2,40)
      

#######################################
#
class UserPlayer(Player):
#######################################
  def __init__(self, name=''):
    Player.__init__(self, name)
    self.name = 'Felseged, ' + name

  def emel(self):
    return int( my_input("Hol emeled el? [2--40] ") )
  
  def select(self, sofar):
    selected = False
    if sofar: 
      print "Eddig",sofar,
    
    handShown = False
    while not selected:
      crd = my_input("Melyiket teszed? ")
      for card in self.cards:
        if crd.upper() == str(card):
          selected = True
          break
      if not (selected or handShown):
        print ' -'*10+"  Kartyaid:", self.cards
        handShown = True
      
      # to check against rules
    return card

  def showCards(self):
    s = str(self.cards)
    stars = "*" *(len(s)+4)
    print stars
    print "*", s, "*"
    print "*", ' '*len(s), "*"
    print stars
 