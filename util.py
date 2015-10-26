#######################################
#
#  utility stuff: 
#   - Symbols, 
#   - processing a sequence of tasks
#   - my_input using raw_input
#   - @buildOnObject decorator
#
#######################################

_globals = globals()

class Symbol(object):
  def __init__(self, name, idx):
    self.name = name
    self.index = idx
  def __repr__(self):
    return "(symbol)%s" % self.name
  def __str__(self):
    return self.name
  def __lt__(self, other):
    return self.index < other.index

class ShiftedList(list):
  def __init__(self, iterable=[], shift=0):
    list.__init__(self, iterable)
    self.start = shift
  def shift(self, num):
    self.start += num
  def _diff(self, idx):
    return (idx - self.start)
  def __getitem__(self, idx):
    return list.__getitem__(self, self._diff(idx))
  def __setitem__(self, idx, value):
    return list.__setitem__(self, self._diff(idx), value)
  def __getslice__(self, start, end):
    return list.__getslice__(self, self._diff(start), self._diff(end))
  def __setslice__(self, start, end, value):
    return list.__setslice__(self, self._diff(start), self._diff(end), value)

def Symbols(*symbols,**instructions):
  ''' use  addSymbolsTo(globals())  or  addSymbolsTo(locals()) before first usage '''
  global _globals

  idx = instructions.get('start', 1)
  symGroup = ShiftedList(shift=idx)
  for sym in symbols:
    _globals[sym] = Symbol(sym, idx)
    symGroup.append( _globals[sym] )
    idx += 1
  return symGroup

def addSymbolsTo(namespace):
  ''' This method is needed before usage of Symbols if module is imported. 
Usage:  addSymbolsTo(globals())
    or  addSymbolsTo(locals()) '''
  global _globals
  _globals = namespace 

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
      if Decorated._fromBaseObj(self, attr) == notFromBase:
        cls.__setattr__(self, attr, value)
        return
      setattr(Decorated._baseObjs[self], attr, value)

    def __delattr__(self, attr):
      if Decorated._fromBaseObj(self, attr) == notFromBase:
        cls.__delattr__(self, attr)
        return
      delattr(Decorated._baseObjs[self], attr)

  return Decorated
