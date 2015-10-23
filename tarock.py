'''Tarokk'''

class Symbol(object):
  def __init__(self, name, idx):
    self.name = name
    self.index = idx
  def __repr__(self):
    return self.name

def Symbols(*symbols,**instructions):
  idx = instructions.get('start', 1)
  symGroup = {}
  for sym in symbols:
    globals()[sym] = symGroup[idx] = Symbol(sym, idx)
    idx += 1
  return symGroup

class Card:
  # CONSTS
  # figures
  colors = Symbols('TAROKK','TREFF','KARO','PIKK','KOR', start=0)
  figures = Symbols('ASZ','BOTOS','LOVAS','DAMA','KIRALY')
  tarocks = Symbols('I','II','III','IIII','V','VI','VII','VIII','IX','X',
                    'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII',
                    'XIX','XX','XXI','SKIZ')
  
  def __init__(my, color, num):
    my.color = color
    my.num = num
    my.isTarock = (color==TAROKK)
    my.isHonour = False
    if my.isTarock:
      if num in {I,XXI,SKIZ}: 
        my.value = 5
        my.isHonour = True
      else: 
        my.value = 1
    else:
      my.value = num.index
  
  def __repr__(me):
    if me.isTarock: return me.num
    else: return "%s %s" %(me.color, me.num)
  
  @staticmethod
  def random():
    # to randomize -- would we ever need it?
    return Card(SPADES, KING)

class Deck(list):
  def __init__(self, arg=None):
    if arg:
      list.__init__(self, arg)
    else:
      list.__init__(self, Card.tarocks.values())

class Party:
  # phases: 
  OSZT, LICIT, SKART, BEMOND, LEJATSZ, FIZET = range(6)
  
  def __init__(self):
    deck = Deck() # to move it to class Table, later
  
  def oszt(self):
    # 6 talon
    pass
    