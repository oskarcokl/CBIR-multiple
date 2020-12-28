import os

from flask import Flask, render_template, request, jsonify

import numpy as np
from simple_color_search.colordescriptor  import ColorDescriptor
from simple_color_search.searcher import Searcher


# Create flast instance
app = Flask(__name__)
app.config["DEBUG"] = True

INDEX_SIMPLE = os.path.join(os.path.dirname(__file__), "./simple_color_search/index.csv")
INDEX_BOVW = os.path.join(os.path.dirname(__file__), "./bovw_sift/index.csv")
CLUSTER=os.path.join(os.path.dirname(__file__), "./bovw_sift/train_k_means.joblib")


# Main route
@app.route("/")
def index():
    return render_template("index.html")

# Basic search route
@app.route("/basic-search", methods=["POST"])
def basic_search():
    if request.method == "POST":

        RESULTS_ARRAY = []
        filestr = request.files["img"].read()

        try:

            # Initialize the colordescriptor
            colorDescriptor = ColorDescriptor((8, 12, 3))

            # Load querry image and describe it
            from skimage import io
            import cv2

            npimg = np.frombuffer(filestr, np.uint8)

            # Query image is already in BGR
            query = cv2.imdecode(npimg, -1)

            features = colorDescriptor.describe(query)


            # Perform search
            searcher = Searcher(INDEX)
            results  = searcher.search(features)

            # Loop over the results and displaying score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)}
                    )


            return jsonify(results=RESULTS_ARRAY[:10])

        except:

            # Return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# BoVW search route
@app.route("/bovw-search", methods=["POST"])
def bovw_search(): 
    if request.method == "POST":

        RESULTS_ARRAY = []

        filestr = request.files["img"].read()

        try: 
            # Initialize the colordescriptor
            siftDescriptor = SiftDescriptor()
            histogramBuilder = HistogramBuilder()
            # TODO change name of Searcher objects so there isn't a conflict.
            searcher = Searcher(INDEX_BOVW)

            # Load querry image and describe it
            import cv2

            npimg = np.frombuffer(filestr, np.uint8)
            # Query image is already in BGR
            query_image = cv2.imdecode(npimg, -1)
            query_image_grayscale = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
            descriptors = siftDescriptor.describe(query_image_grayscale)
            
            clusters = load(CLUSTER)
            query_histogram = historgamBuilder.buil_histogram_from_clusters(dscriptors, clusters)

            (distances, image_ids) = searcher.search(query_histogram, 10)

            # Loop over the results and displaying score and image name
            for i in len(image_ids):
                RESULTS_ARRAY.append(
                    {"image": str(image_ids[i]), "score": str(distances[i])}
                    )


            return jsonify(results=RESULTS_ARRAY[:10])

        except:

            # Return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500
    print("You are searching with BOVW")


# Run!
if __name__ == "__main__":
    app.run()
