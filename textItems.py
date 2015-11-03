
from importlib import import_module

language = 'ENG'
namespace = {}

def setLang(lang):
  global language
  if lang!=language:
    if getDict(lang):
      language = lang

def getDict(lang):
  global namespace
  try:
    myDict = import_module('my_%s_dict' % lang)
    for v in dir(myDict):
      if not v.startswith('__'):
        namespace[v] = getattr(myDict, v)
    return True
  except ImportError:
    print("No {0} dictionary found (file 'my_{0}_dict.py').\n"
          "You can create one by  translate.py.\n\n".format(lang))
  return False

def addTo(_namespace):
  global namespace
  namespace = _namespace
  # init
  setLang(language)

