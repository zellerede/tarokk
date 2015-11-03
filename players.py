from random import randint, choice

from deck import *
from util import my_input, Cash
import textItems
textItems.addTo(globals())


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
    self.cash = Cash(200)
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
    display("^"*42)
    display(" "*8, self, "wearing the HAT")
    display("v"*42)

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
    self.name = _Your_majesty_ + name

  def emel(self):
    return int( my_input(_Where_to_split_the_deck___2__40__) )
  
  def select(self, sofar):
    selected = False
    if sofar: 
      display(_So_far,sofar, continueLine=True)
    
    handShown = False
    while not selected:
      crd = my_input(_Which_card_to_call__)
      for card in self.cards:
        if crd.upper() == str(card):
          selected = True
          break
      if not (selected or handShown):
        display(' -'*10+_Your_cards_, self.cards)
        handShown = True
      
      # to check against rules
    return card

  def selectToSkart(self, someCards):
    selected = False
    helpShown = handShown = False
    while not selected:
      crd = my_input(_Choose_one_to_discard__)
      for card in someCards:
        if crd.upper() == str(card):
          selected = True
          break
      if not (selected or helpShown):
        display(' -'*10+_You_can_choose_among_, someCards)
        helpShown = True
      elif not (selected or handShown):
        display(' -'*10+_Your_cards_, self.cards)
        handShown = True
      # to check against rules
    return card

  def licit(self):
    draw = ''
    while not draw:
      draw = my_input(_How_many_cards_to_claim___0__3____)
    return int(draw)

  def showCards(self):
    s = str(self.cards)
    stars = "*" *(len(s)+4)
    display(stars)
    print "*", s, "*"
    print "*", ' '*len(s), "*"
    display(stars)
 
  def askPartner(self):
    selected = False
    while not selected:
      crd = my_input(_Choose_your_partner_by_a_card__)
      if crd:
        try:
          num = eval(crd.strip().upper())
          selected = True
        except NameError:
          pass
    return Card(num)
    

