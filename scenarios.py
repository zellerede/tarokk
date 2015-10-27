''' Tarock figures, i.e. play scenarios '''
from util import buildOnObject
from deck import *

@buildOnObject # of class Party
class Scenario(object):
  pass

class Parti(Scenario):
  def getWinner(self):
    challenged = self._calcHitsOf(self.challengers)
    print "-"*32
    enemy = self._calcHitsOf(self.poors)
    challengersWon = (challenged >= enemy)
    print "Felvevok", {True:"nyertek", False:"vesztettek"}[challengersWon]
    return {True:self.challengers, False:self.poors}[challengersWon]

  def _calcHitsOf(self, team):
    for p in team:
      s = sum([h.value for h in p.hits])
      print p, "vitt:", s
    summ = sum([c.value for c in team.hits])
    print "Szumma", summ, "pont"
    return summ

class Tuletroa(Scenario):
  def getWinner(self):
    for team in self.teams:
      # print team, "\n    ", team.hits
      if Card.honours <= set(team.hits):
        print "Tuletroa!", team
        return team

class Negykiraly(Scenario):
  cards = {Card(KIRALY, PIKK),
           Card(KIRALY, TREFF),
           Card(KIRALY, KARO),
           Card(KIRALY, KOR)}
  def getWinner(self):
    for team in self.teams:
      if Negykiraly.cards <= set(team.hits):
        print "Negykiraly!", team
        return team

# class XXI_fogas(Scenario):
#   def getWinner(self):


SCENARIOS = (Parti, Tuletroa, Negykiraly) #  Duplajatek, Volat, Pagatultimo
