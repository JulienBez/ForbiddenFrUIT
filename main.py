from scripts.manageFile import *
from scripts.makeAnnotationCSV import *
from scripts.convertCSVtoJSON import *

def proceed(args):
  
  if args.make:
    createSamples()

  if args.convert:
    convertSamples()

if __name__ == "__main__":
	
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("-m", "--make", action="store_true", help="Creates ready-to-annotate CSV files.")
  parser.add_argument("-c", "--convert", action="store_true", help="Convert CSV files to JSON.")

  args = parser.parse_args()
  proceed(args)