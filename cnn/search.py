from searcher import Searcher
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import csv
import cv2
import tensorflow as tf
import numpy as np
import argparse
import os

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--index", required=True,
    help="Path to the index file")
argParser.add_argument("-q", "--query", required=True,
    help="Path to the query image")
argParser.add_argument("-r", "--result_path", required=True,
    help="Path to the result path")
args = vars(argParser.parse_args())

if os.path.isdir("vgg16"):
    model = keras.models.load_model("vgg16")
else:
    model = VGG16(weights="imagenet", include_top=False)

searcher = Searcher(args["index"])
    
img_path = args["query"]
img = image.load_img(img_path, target_size=(244, 244))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

query_features = model.predict(img_array)
features_numpy = np.array(query_features)

(dist, img_ids) = searcher.search(features_numpy.flatten(), 10)

query_img = cv2.imread(img_path)
query_resized = cv2.resize(query_img, (720, 480))
cv2.imshow("Query", query_resized)

print(dist)


for img_id in img_ids:
    result_img = cv2.imread(args["result_path"] + img_id)
    result_resized = cv2.resize(result_img, (720, 480))
    cv2.imshow("Result", result_resized)
    cv2.waitKey(0)
