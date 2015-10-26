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

def my_input(*args, **kws):
  x = raw_input(*args, **kws)
  if x in ['q', 'Q', 'quit', 'Quit']:
    raise Exception("See you")
  return x

#######################################

def buildOn(obj):
  '''decorator buildOn an object'''
  notFromBase = object()
  def fromBaseObj(attr):
    return getattr(obj, attr, notFromBase)

  def decorate(cls):
    class Decorated(cls):
      def __getattribute__(self,attr):
        val = fromBaseObj(attr)
        if val == notFromBase:
          return cls.__getattribute__(self,attr)
        return val
      def __setattr__(self,attr,value):
        if fromBaseObj(attr) == notFromBase:
          cls.__setattr__(self,attr,value)
          return
        setattr(obj,attr,value)
      # __delattr__ ... noo explicitly used I guess
    return Decorated
  return decorate
 