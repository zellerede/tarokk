'''Fast translate once all string literals'''

import os
import re

# myDict = {}

def translateAllFilesAround(path='.', lang=''):
  for (subPath, _, files) in os.walk(path):
    for fileName in files:
      if fileName.endswith('.py'):
        translateFile( os.path.join(subPath, fileName) )
  writeDict('my%sDict.py' % lang)

def translateFile(fileName):
  with open(fileName) as f:
    content = f.read()
  strLiterals = re.findall(r'''(['"])(.*?)\1''', content)
  for apost,literal in strLiterals:
    translation = askTranslation(literal)
    if translation:
      myDict[literal] = translation
      print apost+literal+apost
      content = content.replace(apost+literal+apost, underscored(translation) )
  with open('trans/'+fileName, 'w') as f:
    f.write(content)

def askTranslation(expression):
  if expression in myDict:
    return myDict[expr]
  # return raw_input("Translate '%s'\n---------- " % expression)


def underscored(text):
  text = '_' + re.sub(r'[ :\[\]\\()\-\*\?!\.,]', '_', text)
  return text

def writeDict(fileName):
  with open(fileName,'w') as f:
    for expr, transl in myDict.items():
      f.write("%s = '%s'\n" %(underscored(transl), expr))
