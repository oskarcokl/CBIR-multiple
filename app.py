import os

from flask import Flask, render_template, request, jsonify

import numpy as np
from joblib import load
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image

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
CLUSTER=os.path.join(os.path.dirname(__file__), "./bovw_sift/train_k_means.joblib")


# Main route
@app.route("/")
def index():
    return render_template("index.html")

# All search
@app.route("/all-search", methods=["POST"])
def all_search():

    # Can reach the endpoint
    print("You are searching with all of the algorythms.")
    

    return ""
    
# Basic search route
@app.route("/simple-search", methods=["POST"])
def basic():
    if request.method == "POST":

        filestr = request.files["img"].read()

        return basic_search(filestr);
        
        


# BoVW search route
@app.route("/bovw-search", methods=["POST"])
def bovw(): 
    if request.method == "POST":

        RESULTS_ARRAY = []
        
        filestr = request.files["img"].read()

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


            return jsonify(results=RESULTS_ARRAY[:10])

        except Exception as inst:
            print(inst)
            
            # Return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


@app.route("/cnn-search", methods=["POST"])
def cnn():
    if request.method == "POST":
        RESULTS_ARRAY = []
        filestr = request.files["img"].read()

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


            return jsonify(results=RESULTS_ARRAY[:10])
        except:
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500            

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


        return jsonify(results=RESULTS_ARRAY[:10])

    except Exception as inst:

        print(inst)

        # Return error
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
            
            
# Run!
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
