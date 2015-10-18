'''Tarokk'''

class Card:
  # CONSTS
  # figures
  ASZ = TEN = 1
  BOTOS     = 2 #eng?
  LOVAS     = 3
  DAMA      = 4
  KIRALY    = 5
  SKIZ      = 22 #eng?
  # colors
  TAROCK, CLUBS, DIAMONDS, SPADES, HEARTS = range(5)
  
  def __init__(my, color, num):
    my.color = color
    my.num = num
    my.tarock = (color==TAROCK)
    my.isHonour = False
    if my.isTarock:
      if num in {1,21,22}: 
        my.value = 5
        my.isHonour = True
      else: 
        my.value = 1
    else:
      my.value = num
  
  @staticmethod
  def random():
    # to randomize -- would we ever need it?
    return Card(SPADES, KING)
    

class Party:
  # phases: LICIT, SKART, BEMOND, LEJATSZ, FIZET
  