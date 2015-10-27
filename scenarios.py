''' Tarock figures, i.e. play scenarios '''
from util import buildOnObject
from deck import *

@buildOnObject # of class Party
class Scenario(object):
  def investigate(self):
    winnerTeam = self.getWinner()
    if winnerTeam:
      print type(self).__name__+"!", winnerTeam


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
    type(self).__name__ = 'XXI-es fogas'
    for rundo in self.rounds:
      if self.cards <= set(rundo):
        return self.teamOf(rundo.winner)
        #print "XXI-es fogas!", team

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
    if round2check.winnerCard in self.cards:
      return self.teamOf(round2check.winner)

class Pagat:
  cards = {Card(I)}

class Sas:
  cards = {Card(II)}

class Kiraly:
  cards = Card.kings

class Pagatultimo(Pagat, Ultimi): pass
class Sasultimo(Sas, Ultimi): pass
class Kiralyultimo(Ultimi): pass

class Uhu(Ultimi):
  roundIdx = -2 # one before last
 
class Pagatuhu(Pagat, Uhu): pass
class Sasuhu(Sas, Uhu): pass
class Kiralyuhu(Kiraly, Uhu): pass

class Facan(Ultimi):
  roundIdx = 0 # first round

class Pagatfacan(Pagat, Facan): pass
class Sasfacan(Sas, Facan): pass

SCENARIOS = (Parti, Tuletroa, Negykiraly, Duplajatek, XXI_fogas, Volat, Pagatultimo, 
             Sasultimo, Kiralyultimo, Pagatuhu, Sasuhu, Pagatfacan, Sasfacan) 
     # plusz akar:
     # -- tuletroa-rundo
     # -- whatsoever
