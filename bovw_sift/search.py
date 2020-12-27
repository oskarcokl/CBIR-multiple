from sift_descriptor import SiftDescriptor
from searcher import Searcher
from image_loader import ImageLoader
import argparse
from k_means import MyKMeans
from histogram_builder import HistogramBuilder 
import cv2
from joblib import dump, load
import csv

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--index", required=True,
    help="Path to the index file")
argParser.add_argument("-q", "--query", required=True,
    help="Path to the query image")
argParser.add_argument("-r", "--result_path", required=True,
    help="Path to the result path")

args = vars(argParser.parse_args())

# Initialize siftDescriptor
siftDescriptor = SiftDescriptor()
histogramBuilder = HistogramBuilder()
searcher = Searcher(args["index"])

query_image = cv2.imread(args["query"])
query_image_grayscale = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)

descriptors = siftDescriptor.describe(query_image_grayscale)

clusters = load("train_k_means.joblib")
query_histogram = histogramBuilder.build_histogram_from_clusters(descriptors, clusters)

(distance, results) = searcher.search(query_histogram, 10)

query_resized = cv2.resize(query_image, (720, 480))
cv2.imshow("Query", query_resized)


with open(args["index"]) as index:
    csvReader = csv.reader(index)
    image_ids = [row[0] for row in csv.reader(index)]
index.close()

for result in results[0]:
    result_image = cv2.imread(args["result_path"] + image_ids[result])
    result_resized = cv2.resize(result_image, (720, 480))
    cv2.imshow("Result", result_resized)
    cv2.waitKey(0)
