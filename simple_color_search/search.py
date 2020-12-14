from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2

# Construct the arguments parser and pars the arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--index", required=True,
    help="Path to the index file")
argParser.add_argument("-q", "--query", required=True,
    help="Path to the query image")
argParser.add_argument("-r", "--result-path", required=True,
    help="Path to the result path")

args = vars(argParser.parse_args())

# Initialize image descriptor
cd = ColorDescriptor((8, 12, 3))

# Load query image and describe it 
query = cv2.imread(args["query"])
featurse = cd.describe(query)

# Perform the search
searcher = Searcher(args["idnex"])