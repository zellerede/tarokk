
# English
import my_ENG_Dict as myDict

# Hungarian
# import my_HUN_Dict as myDict

def addTo(namespace):
  for v in dir(myDict):
    if v not in ['__name__', '__dict__']:
      namespace[v] = getattr(myDict, v)

