import json

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data


def writeJson(path,data):
  "create a json file"
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)


def openCSV(path):
  "open our csv file"
  with open(path,"r",encoding="utf-8") as f:
    data = f.readlines()
  return data


def writeCSV(path,data):
  "write our csv file"
  with open(path,"w",encoding="UTF-8") as f:
    for line in data:
      f.write(line)