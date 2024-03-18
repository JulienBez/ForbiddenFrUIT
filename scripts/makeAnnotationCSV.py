import re
import os

from .manageFile import * 

def segmentWords(string):
  "segment a tweet in a list of word and handle some char"

  replace = re.findall("(?P<url>https?://[^\s]+)", string) + re.findall("[\.\!\?][\.\!\?]+",string)
  for url in replace:
    string = string.replace(url," <URLTEMP> ") 

  toRemove = ["'","’","`","\n","\r","\t"]
  toIsolate = [".","?","!",'"',";",",",":",")","(","]","["]

  for tr in toRemove:
    string = string.replace(tr," ")
  for ti in toIsolate:
    string = string.replace(ti,f" {ti} ")
  string_list = re.sub(' +', ' ', string).split(" ")

  for url in replace:
    for i,s in enumerate(string_list):
      if s == "<URLTEMP>":
        string_list[i] = url
        break
      
  return [s for s in string_list if s!="" and s!=" "]

def escape(string):
  "helps to make a well formated csv file by escaping everything"
  return f'''"{string.replace('"', '""')}"'''

def getUMWEannotated(data):
  "get every tweet annotated as containing an UMWE an put them in  columns"
  umwes = []
  seeds = list(set([v["seed"] for k,v in data.items()]))
  for seed in seeds:
    for k,v in data.items():
      if v["UMWE_identified"] and v["seed"] == seed:
        tw = v["tweet"].replace("\n"," ").replace("\r"," ")
        tweet_line = f'''"id",{escape("'"+k)},\n"tweet",{escape(tw)},\n"seed",{escape(v["seed"])},\n'''
        segmented = segmentWords(v["tweet"])
        for word in segmented:
          tweet_line = tweet_line + f'''{escape(word)},\n'''
        tweet_line = tweet_line + "\n"
        umwes.append(tweet_line)
  return umwes

def createSamples(annotator_number=3):
  "create X exact same samples, X being the number of annotators"
  counter = 0
  data = getUMWEannotated(openJson("data/control_tweets.json"))
  while counter < annotator_number:
    filename = f"data/csv/A{counter+1}_annotations.csv"
    if os.path.isfile(filename) == False:
      writeCSV(filename,data)
    counter += 1