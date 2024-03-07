import re
import string as strii

import spacy
sp = spacy.load("fr_dep_news_trf")

def removePunct(string):
  "map punctuation to space, not used as for now"
  return string.translate(str.maketrans(strii.punctuation, ' '*len(strii.punctuation)))

def spacePunct(string):
  "add spaces before and after punctuation to ease later treatments"
  return string.translate(str.maketrans({key: " {0} ".format(key) for key in strii.punctuation}))

def repBadChar(string):
  "replace problematic characters / punctuation with space"
  bad_char = ["'","’","-","\n","\r",";"]
  for bc in bad_char:
    string = string.replace(bc," ")
  return re.sub(' +', ' ', string)

def noEmpty(word):
  "check if a tag is empty or not"
  return word if word else "_"

def tokenizer(text):
  "tokenize everything in a given spacy object"
  text_sp = [i for i in sp(spacePunct(repBadChar(text).lower())) if i.pos_ != "SPACE"]
  return [noEmpty(word.text) for word in text_sp]
