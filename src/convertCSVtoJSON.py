import glob

from .manageFile import *

def getAnnotations(path):
  "get annotations from csv and put them in json"

  lines = openCSV(path)
  splitLines = []

  for l in lines:
    if l == "\n" or l == ",\n":
      l = "<SPLITHERE>"
    splitLines.append(l)
  if splitLines[-1] == "<SPLITHERE>":
    splitLines.pop()

  dict_annot = {}
  splitLines = "".join(splitLines).split("<SPLITHERE>")

  for i in splitLines:
    j = i.split("\n")
    id_tweet = "".join([a for a in j[0] if a.isnumeric() == True])
    words = [w.replace('""','<GUILLEMETS>').replace('"','').replace("<GUILLEMETS>",'"').replace('""','"').replace(",,","<TRUEVIRG>,") for w in j[3:]]
    dict_annot[id_tweet] = {"words":[],"annots":[]}

    for word in words:
      temp = word.split(",")
      w = temp[0].replace("<TRUEVIRG>",",")
      a = ",".join(temp[1:]).replace("<TRUEVIRG>",",")
      dict_annot[id_tweet]["words"].append(w)
      dict_annot[id_tweet]["annots"].append(a)

  writeJson(path.replace("csv","json"),dict_annot)


def control(path):
  "check if we have all the tweets"
  control_list = [k for k,v in openJson("data/control_tweets.json").items() if v["UMWE_identified"]==True]
  test_list = [k for k,v in openJson(path.replace("csv","json")).items()]
  for i in control_list:
    if i not in test_list:
      print(path)
      print(i)


def convertSamples():
  "convert annotated samples from CSV to JSON"
  for path in glob.glob("data/csv/*.csv"):
    getAnnotations(path)
    control(path)