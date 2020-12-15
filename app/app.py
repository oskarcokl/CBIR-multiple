import os

from flask import Flask, render_template, request, jsonify

from simple_color_search.colordescriptor  import ColorDescriptor
from simple_color_search.searcher import Searcher


# Create flast instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), "./simple_color_search/index.csv")

# Main route
@app.route("/")
def index():
    return render_template("index.html")

# search route
@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":

        RESULTS_ARRAY = []

        # Get image URL
        image_url = request.form.get("img")

        try:

            # Initialize the colordescriptor
            colorDescriptor = ColorDescriptor((8, 12, 3))

            # Load querry image and describe it
            from skimage import io
            import cv2
            query = io.imread(image_url)
            query = (query * 255).astype("uint8")
            # (b, g, r) get transformed into (h, s, v) in the code
            (r, g, b) = cv2.split(query)
            query = cv2.merge([b, g, r])
            features = colorDescriptor.describe(query)

            # Perform search
            searcher = Searcher(INDEX)
            results  = searcher.search(features)

            # Loop over the results and displaying score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)}
                    )


            # Return top 3 results
            return jsonify(results=RESULTS_ARRAY[::-1])

        except:

            # Return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500

# Run!
if __name__ == "__main__":
    app.run(debug=True)
