'''Fast translate once all string literals'''

import os
import re

if 'myDict' not in globals():
  myDict = {}

def translateFile(fileName, resultFile):
  with open(fileName) as f:
    content = f.read()
  strLiterals = re.findall(r'''(['"])(.*?)\1''', content)
  for _,literal in strLiterals:
    translation = askTranslation(literal)
    if translation:
      myDict[literal] = translation
      content = content.replace(literal, translation)
  with open(resultFile, 'w') as f:
    f.write(content)

def askTranslation(expression):
  if expression in myDict:
    return myDict[expression]
  return raw_input("Translate '%s'\n---------- " % expression)


def underscored(text):
  text = '_' + re.sub(r'[ :\[\]\\()\-\*\?!\.,]', '_', text)
  return text

if __name__ == '__main__':
  translateFile('my_ENG_Dict.py', 'my_Dict.py')
  print myDict
