import re
import glob
import json

#from scripts.NLP import *

def segmentWords(string):
  ""

  replace = re.findall("(?P<url>https?://[^\s]+)", string) + re.findall("[\.\!\?][\.\!\?]+",string)
  for url in replace:
    string = string.replace(url," <URLTEMP> ") 

  toRemove = ["'","’","`","\n","\r","\t"]
  toIsolate = [".","?","!",'"',";",",",":",")","(","]","["]
  toKeep = ["#","$","%","@","_","-"]

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

  return string_list

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data

def listToCSV(data):
  "convert list to csv"
  with open("test.csv","w",encoding="UTF-8") as f:
    for line in data:
      f.write(line)

def escape(s:str) -> str:
  return f'''"{s.replace('"', '""')}"'''
  
def getUMWEannotated(data):
  "get every tweet annotated as containing an UMWE"
  umwes = []
  seeds = list(set([v["seed"] for k,v in data.items()]))
  for seed in seeds:
    for k,v in data.items():
      if v["UMWE_identified"] and v["seed"] == seed:
        tweet_line = f'''"tweet",{escape(v["tweet"])},\n"seed",{escape(v["seed"])},\n"{k}_tweet",{",".join(escape(i) for i in segmentWords(v["tweet"]))}\n"{k}_annot",\n"remarque"\n\n'''
        umwes.append(tweet_line)
  return umwes

def createSamples(annotator_number=3):
  "create X exact same samples, X being the number of annotators"
  data = getUMWEannotated(openJson("data/control_tweets.json"))
  listToCSV(data)

createSamples()

def oneSetencePerLine():
  ""
  data = openJson("data/control_tweets.json")
  umwes = []
  seeds = list(set([v["seed"] for k,v in data.items()]))
  for seed in seeds:
    for k,v in data.items():
      if v["UMWE_identified"] and v["seed"] == seed:
        t = v["tweet"].replace("\n","")
        umwes.append(t+"\n")
  listToCSV(umwes)

#oneSetencePerLine()