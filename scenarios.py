''' Tarock figures, i.e. play scenarios '''
from util import buildOnObject
from deck import *

@buildOnObject # of class Party
class Scenario(object):
  def __init__(self):
    self.name = type(self).__name__

  def investigate(self):
    winnerTeam = self.getWinner()
    if winnerTeam:
      print self.name+"!", winnerTeam

class Parti(Scenario):
  def getWinner(self):
    challenged = self._calcHitsOf(self.challengers)
    print "-"*32
    enemy = self._calcHitsOf(self.poors)
    challengersWon = (challenged > enemy)
    print "Felvevok", {True:"nyertek", False:"vesztettek"}[challengersWon]
    return {True:self.challengers, False:self.poors}[challengersWon]

  def _calcHitsOf(self, team):
    for p in team:
      s = sum([h.value for h in p.hits])
      print p, "vitt:", s
    summ = sum([c.value for c in team.hits])
    print "Szumma", summ, "pont"
    return summ

class Duplajatek(Scenario):
  def getWinner(self):
    for team in self.teams:
      score = sum([c.value for c in team.hits])
      if score < 24:
        return self.otherTeam(team)

class Tuletroa(Scenario):
  def getWinner(self):
    for team in self.teams:
      # print team, "\n    ", team.hits
      if Card.honours <= set(team.hits):
        return team

class Negykiraly(Scenario):
  def getWinner(self):
    for team in self.teams:
      if Card.kings <= set(team.hits):
        return team

class XXI_fogas(Scenario):
  cards = {Card(XXI), Card(SKIZ)}
  def getWinner(self):
    self.name = 'XXI-es fogas'
    for rundo in self.rounds:
      if self.cards <= set(rundo):
        theNewMajor = rundo.whoHad( Card(XXI) )
        self.players[theNewMajor].sapka()
        return self.otherTeam( self.teamOf(theNewMajor) )

class Volat(Scenario):
  def getWinner(self):
    for team in self.teams: # should be 2
      if not sum([p.hits for p in team], []):
        return self.otherTeam(team)

class Ultimi(Scenario):
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
  roundIdx = 0 # first round
  def checkIfTried(self, rundo):
    if rundo[0].color==TAROKK:
      return False, None
    return Ultimi.checkIfTried(self, rundo)

class Pagatfacan(Pagat, Facan): pass
class Sasfacan(Sas, Facan): pass

SCENARIOS = (Parti, Tuletroa, Negykiraly, Duplajatek, XXI_fogas, Volat, Pagatultimo, 
             Sasultimo, Kiralyultimo, Pagatuhu, Sasuhu, Pagatfacan, Sasfacan) 
     # plusz akar:
     # -- tuletroa-rundo
     # -- pagat-rundo, 
     # -- egyszinu-rundo (kiraly v dama visz)
