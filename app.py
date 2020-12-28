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


# Main route
@app.route("/")
def index():
    return render_template("index.html")

# Basic search route
@app.route("/basic-search", methods=["POST"])
def basic_search():
    if request.method == "POST":

        RESULTS_ARRAY = []

        # Get image URL

        print("Hello")

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
            searcher = Searcher(

            # Load querry image and describe it
            from skimage import io
            import cv2

            npimg = np.frombuffer(filestr, np.uint8)

            # Query image is already in BGR
            query = cv2.imdecode(npimg, -1)

            features = colorDescriptor.describe(query)


            # Perform search
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
    print("You are searching with BOVW")


# Run!
if __name__ == "__main__":
    app.run()
