import json

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data

def listToCSV(path,data):
  "convert list to csv"
  with open(path,"w",encoding="UTF-8") as f:
    for line in data:
      f.write(line)