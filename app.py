import os

from flask import Flask, render_template, request, jsonify

import numpy as np
from joblib import load
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import cv2

from simple_color_search.colordescriptor  import ColorDescriptor
from simple_color_search.searcher import Searcher as SearcherSimple

from bovw_sift.searcher import Searcher as SearcherBovw
from bovw_sift.sift_descriptor import SiftDescriptor
from bovw_sift.histogram_builder import HistogramBuilder

from cnn.searcher import Searcher as SearcherCNN

# Create flast instance
app = Flask(__name__)

INDEX_SIMPLE = os.path.join(os.path.dirname(__file__), "./simple_color_search/index.csv")
INDEX_BOVW = os.path.join(os.path.dirname(__file__), "./bovw_sift/index_all.csv")
INDEX_CNN = os.path.join(os.path.dirname(__file__), "./cnn/index.csv")
CLUSTER = os.path.join(os.path.dirname(__file__), "./bovw_sift/train_k_means.joblib")

KNN_CNN = os.path.join(os.path.dirname(__file__), "./cnn/kmeans_model.joblib")
VGG16_CNN = os.path.join(os.path.dirname(__file__), "./cnn/vgg16")

STATIC = os.path.join(os.path.dirname(__file__), "./static/images/")


# Main route
@app.route("/")
def index():
    return render_template("index.html")

# All search
@app.route("/all-search", methods=["POST"])
def all_search():

    if request.method == "POST":
        filestr = request.files["img"].read()
        # Can reach the endpoint
        print("You are searching with all of the algorythms.")
        RESULTS_ARRAY_JSON = []
        
        print("Searching basic")
        RESULTS_ARRAY_JSON.append(basic_search(filestr))
        print("Done basic")
        print("Searching bovw")
        RESULTS_ARRAY_JSON.append(bovw_search(filestr))
        print("Done bovw")
        print("Searching cnn")
        RESULTS_ARRAY_JSON.append(cnn_search(filestr))
        print("Done cnn")
        print("Done searching")        

        return jsonify(basic=RESULTS_ARRAY_JSON[0],
                       bovw=RESULTS_ARRAY_JSON[1],
                       cnn=RESULTS_ARRAY_JSON[2])
    
# Basic search route
@app.route("/simple-search", methods=["POST"])
def basic():
    if request.method == "POST":
        filestr = request.files["img"].read()
        RESULTS_ARRAY = basic_search(filestr);
        return jsonify(results=RESULTS_ARRAY)
        
        
# BoVW search route
@app.route("/bovw-search", methods=["POST"])
def bovw(): 
    if request.method == "POST": 
        filestr = request.files["img"].read()
        RESULTS_ARRAY = bovw_search(filestr)
        return jsonify(results=RESULTS_ARRAY)



@app.route("/cnn-search", methods=["POST"])
def cnn():
    if request.method == "POST":
        filestr = request.files["img"].read()
        RESULTS_ARRAY =  cnn_search(filestr)
        return jsonify(results=RESULTS_ARRAY)

# @app.route("/cnn-index", methods=["POST"])
# def cnn_index():
#     if request.method == "POST":
#         filestr = request.files["img"].read()

#====== INDEX =========#
@app.route("/all-index", methods=["POST"])
def all_index():
    if request.method == "POST":

        images = request.files
        
        #_cnn_index(images)
        #_bovw_index(images)
        _basic_index(images)

        
        # for key in images:
        #     print(key)
        #     print(images[key].filename)

        return ""
        
# filestr is array of image strings
def _cnn_index(images):
    if os.path.isdir(VGG16_CNN):
        model = keras.models.load_model(VGG16_CNN)
        print("Loading local vgg16")
    else:
        model = VGG16(weights="imagenet", include_top=False)
        print("Downloading vgg16")


    index_file = open(INDEX_CNN, "a")  

    for key in images:
        img = images[key]
        img_name = img.filename
        img_path = os.path.join(STATIC, img_name)

        img.save(img_path)

        
        img = image.load_img(img_path, target_size=(244, 244))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        features_numpy = np.array(features)

        #save file to static/images

        write_to_index(features_numpy.flatten(), img_name, index_file)

    index_file.close()
    return


def _bovw_index(images):
    if os.path.isfile(CLUSTER):
        clusters = load(CLUSTER)
    else:
        return jsonify({"message": "Didn't findt local clusters"}, 500);

    index_file = open(INDEX_BOVW, "a")
    histogramBuilder = HistogramBuilder()
    siftDescriptor = SiftDescriptor()

    for key in images:
        img = images[key]
        img_name = img.filename
        img_path = os.path.join(STATIC, img_name)
        img.save(img_path)

        # img_str = img.stream.read()
        # img_np = np.frombuffer(img_str, np.uint8)
        index_img_grayscale = cv2.imread(img_path, 0)
        
        descriptors = siftDescriptor.describe(index_img_grayscale) 
        index_histogram = histogramBuilder.build_histogram_from_clusters(descriptors, clusters)

        #save file to static/images
        
        write_to_index(index_histogram, img_name, index_file)

    index_file.close()
    return
        

    

def _basic_index(images):
    index_file = open(INDEX_SIMPLE, "a")

    colorDescriptor = ColorDescriptor((8, 12, 3))
    
    for key in images:
        img = images[key]
        img_name = img.filename
        img_path = os.path.join(STATIC, img_name)
        img.save(img_path)

        img = cv2.imread(img_path)
        features = colorDescriptor.describe(img)
        features_array = np.array(features)
        
        write_to_index(features_array, img_name, index_file)

    index_file.close()
    return



    

def cnn_search(filestr): 
    RESULTS_ARRAY = []
    try:
        if os.path.isdir("cnn/vgg16"):
            model = keras.models.load_model("cnn/vgg16")
        else:
            model = VGG16(weights="imagenet", include_top=False)

        searcher = SearcherCNN(INDEX_CNN)

        import cv2
        img = np.frombuffer(filestr, np.uint8)
        query_image = cv2.imdecode(img, -1)
        resized_query_image = cv2.resize(query_image, (244, 244))
        img_array = np.expand_dims(resized_query_image, axis=0)

        query_features = model.predict(img_array)
        features_numpy = np.array(query_features)

        print("Hello")

        (dist, img_ids) = searcher.search(features_numpy.flatten(), 10)
        print("Yo this hist works")


        for i in range(len(img_ids)):
            RESULTS_ARRAY.append(
                {"image": str(img_ids[i]), "score": str(dist[i])}
                )


        return RESULTS_ARRAY[:10]
    except:
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500            

    
def bovw_search(filestr): 
    RESULTS_ARRAY = []
    try:
        # Initialize the colordescriptor
        siftDescriptor = SiftDescriptor()
        histogramBuilder = HistogramBuilder()
        searcher = SearcherBovw(INDEX_BOVW)

        # Load querry image and describe it
        import cv2

        npimg = np.frombuffer(filestr, np.uint8)
        # Query image is already in BGR
        query_image = cv2.imdecode(npimg, -1)
        query_image_grayscale = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
        descriptors = siftDescriptor.describe(query_image_grayscale) 
        clusters = load(CLUSTER)

        query_histogram = histogramBuilder.build_histogram_from_clusters(descriptors, clusters)


        (distances, image_ids) = searcher.search(query_histogram, 10)

        # Loop over the results and displaying score and image name
        for i in range(len(image_ids)):
            RESULTS_ARRAY.append(
                {"image": str(image_ids[i]), "score": str(distances[i])}
                )


        return RESULTS_ARRAY[:10]

    except Exception as inst:
        print(inst)

        # Return error
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
            
def basic_search(filestr):
    RESULTS_ARRAY = []

    try:

        # Initialize the colordescriptor
        colorDescriptor = ColorDescriptor((8, 12, 3))

        # Load querry image and describe it
        import cv2

        npimg = np.frombuffer(filestr, np.uint8)

        # Query image is already in BGR
        query = cv2.imdecode(npimg, -1)

        features = colorDescriptor.describe(query)


        # Perform search
        searcher = SearcherSimple(INDEX_SIMPLE)
        results  = searcher.search(features)

        # Loop over the results and displaying score and image name
        for (score, resultID) in results:
            RESULTS_ARRAY.append(
                {"image": str(resultID), "score": str(score)}
                )


        return RESULTS_ARRAY[:10]

    except Exception as inst:

        print(inst)

        # Return error
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
            
def write_to_index(features, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(features.astype(str))))
    
# Run!
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
