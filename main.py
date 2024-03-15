from scripts.manageFile import *
from scripts.segmentation import *

#createSamples()
lines = openCSV("data/csv/A1_annotations.csv")
lines2 = []
for l in lines:
  if l == "\n":
    l = "<SPLITHERE>"
  lines2.append(l)

dict_annot = {}
l2 = "".join(lines2).split("<SPLITHERE>")
for i in l2:
  j = i.split("\n")
  id_tweet = "".join([a for a in j[0] if a.isnumeric() == True])
  words = [w.replace('""','<GUILLEMETS>').replace('"','').replace("<GUILLEMETS>",'"').replace('""','"') for w in j[3:]]
  dict_annot[id_tweet] = words

writeJson("test.json",dict_annot)

  #y'a des tweets avec des \n dedans qui niquent tt -> y'a pu
  #reste à sauver les annotations en simultané pour chaque mot et à créer un fichier json par annotateur dans le dossier data/json/