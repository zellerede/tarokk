from random import randint, choice

from deck import *
from util import my_input

class Players(CycleList):
  def allFrom(self, idx=0):
    for i in self.indicesFrom(idx):
      yield self[i]
  
  all = allFrom
  
  def indicesFrom(self, idx=0):
    for i in range(idx, idx+4):
      yield i % len(self)
  
  def __sub__(self, sub):
    rest = Players(self)
    for x in sub:
      if x in self:
        rest.remove(x)
    return rest

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
  
  def fektet(self, num):
    fektetett = []
    for i in range(num):
      changeable = [card for card in self.cards if (card.value < 5)]
      card = self.selectToSkart(changeable)
      fektetett.append(card)
      self.cards.remove(card)
    return fektetett
  
  def sapka(self):
    print "^"*42
    print " "*8, self, "wearing the HAT"
    print "v"*42

#######################################
#
class AIPlayer(Player):
#######################################
  def emel(self):
    return randint(2,40)
  
  def askPartner(self):
    tarokks = self.cardsOfColor(TAROKK)
    maybePartner = set(range(2,21)) - {t.num.index for t in tarokks}
    partnerCardValue = max(maybePartner)
    return Card( Card.tarocks[partnerCardValue] )


  def selectToSkart(self, someCards):
    changeThese = [card for card in someCards if (card.color != TAROKK)]
    if changeThese: 
      return choice(changeThese)
    return min(set(someCards)-{Card(II)})

  def selectAmong(self, someCards):
    return choice(someCards)

  def licit(self):
    return choice([3]*2 + [2]*4 + [1]*3 + [0])

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

  def selectToSkart(self, someCards):
    selected = False
    helpShown = handShown = False
    while not selected:
      crd = my_input("Melyiket fekteted? ")
      for card in someCards:
        if crd.upper() == str(card):
          selected = True
          break
      if not (selected or helpShown):
        print ' -'*10+"  Valaszthato:", someCards
        helpShown = True
      elif not (selected or handShown):
        print ' -'*10+"  Kartyaid:", self.cards
        handShown = True
      # to check against rules
    return card

  def licit(self):
    return int(my_input("Hany lapot huznal? [0--3] : "))

  def showCards(self):
    s = str(self.cards)
    stars = "*" *(len(s)+4)
    print stars
    print "*", s, "*"
    print "*", ' '*len(s), "*"
    print stars
 
  def askPartner(self):
    selected = False
    while not selected:
      crd = my_input("Kivel leszel? ")
      try:
        num = eval(crd.strip().upper())
        selected = True
      except NameError:
        pass
    return Card(num)
    

