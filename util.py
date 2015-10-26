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

def buildOnObject(cls):
  '''decorator buildOnObject:

Usage example:

@buildOnObject
class X(superclass):
  ...

x=X(obj,*rest,**kws)
# calls X.__init__(x, *rest, **kws)
# and attaches all attributes directly to the instance of (decorated) X
# so, if obj had  obj.attr = 12, then x.attr will return 12
# and modifying x.attr will directly modify obj.attr
'''
  notFromBase = object()

  class Decorated(cls):
    _baseObjs = {}

    def __init__(self, baseObj, *args, **kws):
      Decorated._baseObjs[self] = baseObj
      Decorated.__name__ == "D_" + cls.__name__
      cls.__init__(self, *args, **kws)

    def _fromBaseObj(self, attr):
      return getattr(Decorated._baseObjs.get(self, None), attr, notFromBase)

    def __getattribute__(self, attr):
      val = Decorated._fromBaseObj(self, attr)
      if val == notFromBase:
        return cls.__getattribute__(self, attr)
      return val

    def __setattr__(self, attr, value):
      global _baseObjs
      if Decorated._fromBaseObj(self, attr) == notFromBase:
        cls.__setattr__(self, attr, value)
        return
      setattr(Decorated._baseObjs[self], attr, value)

    # __delattr__ ... noo explicitly used I guess

  return Decorated
