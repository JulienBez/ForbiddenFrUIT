from src.utils import *
from src.convertCSVtoJSON import *
from src.makeAnnotationCSV import *
from src.metadataAnnotation import *

def proceed(args):

	if args.metadata:
		getMetadata()
    
	if args.make:
		createSamples()
		
	if args.convert:
		convertSamples()
    

if __name__ == "__main__":
	
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("-M", "--metadata", action="store_true", help="Get metadata from the annotations made.")
	parser.add_argument("-m", "--make", action="store_true", help="Creates ready-to-annotate CSV files.")
	parser.add_argument("-c", "--convert", action="store_true", help="Convert CSV files to JSON.")

	args = parser.parse_args()
	proceed(args)