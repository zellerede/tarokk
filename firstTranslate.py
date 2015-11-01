'''Fast translate once all string literals'''

import os
import re

if 'myDict' not in globals():
  myDict = {}

def translateAllFilesAround(path='.', lang1='', lang2='_'):
  for fileName in os.listdir(path):
    if fileName.endswith('.py'):
      translateFile( os.path.join(path, fileName) )
  writeDict(lang1, lang2)

def translateFile(fileName):
  with open(fileName) as f:
    content = f.read()
  strLiterals = re.findall(r'''(['"])(.*?)\1''', content)
  for apost,literal in strLiterals:
    translation = askTranslation(literal)
    if translation:
      myDict[literal] = translation
      # print apost+literal+apost
      content = content.replace(apost+literal+apost, underscored(translation) )
  with open('trans/'+fileName, 'w') as f:
    f.write(content)

def askTranslation(expression):
  if expression in myDict:
    return myDict[expression]
  return raw_input("Translate '%s'\n---------- " % expression)


def underscored(text):
  text = '_' + re.sub(r'[ :\[\]\\()\-\*\?!\.,]', '_', text)
  return text

def writeDict(lang1, lang2):
  file1 = 'my%sDict.py' % lang1
  with open(file1,'w') as f:
    for expr, transl in myDict.items():
      f.write("%s = '%s'\n" %(underscored(transl), expr))
  file2 = 'my%sDict.py' % lang2
  with open(file2,'w') as f:
    for transl in myDict.values():
      f.write("%s = '%s'\n" %(underscored(transl), transl))

