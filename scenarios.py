''' Tarock figures, i.e. play scenarios '''
from util import buildOnObject
from deck import *

@buildOnObject # of class Party
class Scenario(object):
  earns = 0
  def __init__(self):
    self.name = type(self).__name__

  def investigate(self):
    winnerTeam = self.getWinner()

    payment = self.earns
    # display(type(self), self.promised, type(self) in self.promised)
    if type(self) not in self.promised:
      payment /= 2 # half the payment for silent scenario

    if winnerTeam and payment:
      display(self.name+"!", winnerTeam, ":", Cash(payment))
      for player in winnerTeam:
        # display(player, player.cash, # debug)
        player.cash += payment
      for player in self.otherTeam(winnerTeam):
        # display(player, player.cash, # debug)
        player.cash -= payment
      # display(# debug)

class Parti(Scenario):
  def getWinner(self):
    self.earns = self.partyPay
    challenged = self._calcHitsOf(self.challengers)
    display("-"*32)
    enemy = self._calcHitsOf(self.poors)
    challengersWon = (challenged > enemy)
    display("Felvevok", {True:"nyertek", False:"vesztettek"}[challengersWon])
    return {True:self.challengers, False:self.poors}[challengersWon]

  def _calcHitsOf(self, team):
    for p in team:
      s = sum([h.value for h in p.hits])
      display(p, "vitt:", s)
    summ = sum([c.value for c in team.hits])
    display("Szumma", summ, "pont")
    return summ

class Duplajatek(Scenario):
  def getWinner(self):
    self.earns = self.partyPay * 4
    for team in self.teams:
      score = sum([c.value for c in team.hits])
      if score < 24:
        self.partyPay = 0
        return self.otherTeam(team)

class Volat(Scenario):
  def getWinner(self):
    self.earns = self.partyPay * 6
    for team in self.teams: # should be 2 teams
      if not sum([p.hits for p in team], []):
        self.partyPay = 0
        return self.otherTeam(team)

class Tuletroa(Scenario):
  earns = 2
  def getWinner(self):
    for team in self.teams:
      # display(team, "\n    ", team.hits)
      if Card.honours <= set(team.hits):
        return team

class Negykiraly(Scenario):
  earns = 2
  def getWinner(self):
    for team in self.teams:
      if Card.kings <= set(team.hits):
        return team

class XXI_fogas(Scenario):
  earns = 42
  cards = {Card(XXI), Card(SKIZ)}
  def getWinner(self):
    self.name = 'XXI-es fogas'
    for rundo in self.rounds:
      if self.cards <= set(rundo):
        theNewMajor = rundo.whoHad( Card(XXI) )
        self.players[theNewMajor].sapka()
        return self.otherTeam( self.teamOf(theNewMajor) )

class Ultimi(Scenario):
  earns = 10
  cards = {Card(I), Card(II)} | Card.kings
  roundIdx = -1 # last one
  def getWinner(self):
    round2check = self.rounds[ self.roundIdx ]
    tried, card = self.checkIfTried(round2check)
    if round2check.winnerCard in self.cards:
      return self.teamOf(round2check.winner)
    if tried:
      self.name += " kiserlet"
      return self.otherTeam(
                self.teamOf(round2check.whoHad(card)) )

  def checkIfTried(self, round2check):
    tried = self.cards & set(round2check)
    card = None
    if tried:
      card = list(tried)[0] # should contain exactly 1 element for all of our use cases
    return bool(tried), card


class Pagat:
  cards = {Card(I)}

class Sas:
  cards = {Card(II)}

class Kiraly:
  cards = Card.kings
  def checkIfTried(self, rundo):
    return False, None

class Pagatultimo(Pagat, Ultimi): pass
class Sasultimo(Sas, Ultimi): pass
class Kiralyultimo(Kiraly, Ultimi): pass

class Uhu(Ultimi):
  roundIdx = -2 # one before last
 
class Pagatuhu(Pagat, Uhu): pass
class Sasuhu(Sas, Uhu): pass
class Kiralyuhu(Kiraly, Uhu): pass

class Facan(Ultimi):
  earns = 12  # or 10 again
  roundIdx = 0 # first round
  def checkIfTried(self, rundo):
    if rundo[0].color==TAROKK:
      return False, None
    return Ultimi.checkIfTried(self, rundo)

class Pagatfacan(Pagat, Facan): pass
class Sasfacan(Sas, Facan): pass

SCENARIOS = (Volat, Duplajatek, Parti, Tuletroa, Negykiraly, XXI_fogas, Pagatultimo, 
             Sasultimo, Kiralyultimo, Pagatuhu, Sasuhu, Pagatfacan, Sasfacan) 
     # plusz akar:
     # -- tuletroa-rundo
     # -- pagat-rundo, 
     # -- egyszinu-rundo (kiraly v dama visz)
