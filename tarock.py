'''Tarokk'''

from random import randint, shuffle

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
  
  @staticmethod
  def random():
    # to randomize -- would we ever need it?
    return Card(KIRALY, PIKK)

#######################################
#
class Deck(list):
#######################################
  def __init__(self, arg=None):
    if arg:
      list.__init__(self, arg)
      return
    for color in Card.colors.values():
      if color==TAROKK:
        for tarock in Card.tarocks.values():
          self.append(Card(tarock))
      else:
        for figure in Card.figures.values():
          self.append(Card(figure, color))

#######################################
#
class Table(object):
#######################################
  def __init__(self):
    self.deck = Deck()
    self.players = ['Eszak', 'Nyugat', 'Del', 'Kelet']
    self.base = 1 # one unit of money
    # etc.
 
  def newParty(self):
    Party(self)

#######################################
#
class Party(object):
#######################################
  # phases = Symbols('KEVER', 'EMEL', 'OSZT', 'LICIT', 'SKART', 'BEMOND', 'LEJATSZ', 'FIZET')
  
  def __init__(Q, table):
    Q.table = table
    process(Q.kever, Q.emel, Q.oszt, Q.licit, Q.skart, Q.bemond, Q.lejatsz, Q.fizet)
  
  def kever(self):
    n = randint(1,8)
    for i in range(n):
      shuffle(self.table.deck)
    # debug
    print self.table.deck
  
  def emel(self):
    pass
  
  def oszt(self):
    # 6 talon
    pass
  
  def licit(self):
    pass
    
  def skart(self):
    pass
  
  def bemond(self):
    pass
  
  def lejatsz(self):
    pass
    
  def fizet(self):
    pass

  _phases = [kever, emel, oszt, licit, skart, bemond, lejatsz, fizet]


#######################################
#
if __name__ == '__main__':
#######################################
  table = Table()
  table.newParty()
