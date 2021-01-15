import tensorflow as tf
import os
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.cluster import KMeans
from joblib import dump, load
import numpy as np
import argparse

def index():
    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-d", "--dataset", required=True,
        help="Path to directory that contains the images to be indexed")
    argParser.add_argument("-i", "--index", 
       help="Path to where teh computed idnex will be stored")
    argParser.add_argument("-t", "--training", action="store_const", const="train",
                           help="If you want to jus train the knn model no csv file will be created")
    args = vars(argParser.parse_args())



    if os.path.isdir("vgg16"):
        model = keras.models.load_model("vgg16")
    else:
        model = VGG16(weights="imagenet", include_top=False)

    
    if args["training"] == "train":
        print("training")
        train_kmeans(args, model)
    else:
        build_index(args, model)



def build_index(args, model):
    if os.path.isfile("kmeans_model.joblib"):
        kmeans_model = load("kmeans_model.joblib")
    else:
        print("No k_means file found")
        return

    data_path = args["dataset"]
    index_file = open(args["index"], "w")
    feature_list = []

    for img_name in os.listdir(data_path):
        img_path = data_path + img_name

        img = image.load_img(img_path, target_size=(244, 244))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        features_numpy = np.array(features)

        write_to_index(features_numpy.flatten(), img_name, index_file)
    print("Finished building index.csv file")

    



def write_to_index(histogram, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(histogram.astype(str))))

        
def train_kmeans(args, model): 
    data_path = args["dataset"]
    feature_list = []

    for img_name in os.listdir(data_path):
        img_path = data_path + img_name

        img = image.load_img(img_path, target_size=(244, 244))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        features_numpy = np.array(features)
        feature_list.append(features_numpy.flatten())

    feature_array = np.array(feature_list)
    kmeans_model = KMeans(n_clusters=700)
    kmeans_model.fit(feature_array)
    dump(kmeans_model, "kmeans_model.joblib")

index()
