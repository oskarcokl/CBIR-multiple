import os

from flask import Flask, render_template, request, jsonify

import numpy as np
from colorama import init, Fore, Back
import csv
from joblib import load
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import cv2
import json

from simple_color_search.colordescriptor  import ColorDescriptor
from simple_color_search.searcher import Searcher as SearcherSimple

from bovw_sift.searcher import Searcher as SearcherBovw
from bovw_sift.sift_descriptor import SiftDescriptor
from bovw_sift.histogram_builder import HistogramBuilder

from cnn.searcher import Searcher as SearcherCNN

# Create flast instance
app = Flask(__name__)
init()

INDEX_SIMPLE = os.path.join(os.path.dirname(__file__), "./simple_color_search/index.csv")
INDEX_BOVW = os.path.join(os.path.dirname(__file__), "./bovw_sift/index.csv")
INDEX_CNN = os.path.join(os.path.dirname(__file__), "./cnn/index.csv")
CLUSTER = os.path.join(os.path.dirname(__file__), "./bovw_sift/train_k_means.joblib")

KNN_CNN = os.path.join(os.path.dirname(__file__), "./cnn/kmeans_model.joblib")
VGG16_CNN = os.path.join(os.path.dirname(__file__), "./cnn/vgg16")

STATIC = os.path.join(os.path.dirname(__file__), "./static/images/")


results_bovw = []
results_cnn = []
results_simple = []
curr_query_bovw = []
curr_query_cnn = []
global curr_query_simple


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

        print(RESULTS_ARRAY_JSON[0])
        print(RESULTS_ARRAY_JSON[1])
        print(RESULTS_ARRAY_JSON[2])

        response = jsonify({"basic" : RESULTS_ARRAY_JSON[0],
                           "bovw" : RESULTS_ARRAY_JSON[1],
                            "cnn" : RESULTS_ARRAY_JSON[2]}, 200)
        
        return response


def _all_search(query_basic, query_bovw, query_cnn):

    # Can reach the endpoint
    print("You are searching with all of the algorythms.")
    RESULTS_ARRAY_JSON = []

    print("Searching basic")
    RESULTS_ARRAY_JSON.append(basic_search_query(query_basic))
    print("Done basic")

    # TODO remember to unccoment later

    print("Searching bovw")
    RESULTS_ARRAY_JSON.append(bovw_search_query(query_bovw))
    print("Done bovw")
    print("Searching cnn")
    RESULTS_ARRAY_JSON.append(cnn_search_query(query_cnn))
    print("Done cnn")
    print("Done searching")


    return jsonify({"basic": RESULTS_ARRAY_JSON[0],
                    "bovw": RESULTS_ARRAY_JSON[1],
                    "cnn": RESULTS_ARRAY_JSON[2]}, 200)

    
# Basic search route
@app.route("/simple-search", methods=["POST"])
def basic():
    if request.method == "POST":
        filestr = request.files["img"].read()
        RESULTS_ARRAY = basic_search(filestr);
        results_simple = RESULTS_ARRAY
        return jsonify(results=RESULTS_ARRAY)
        
        
# BoVW search route
@app.route("/bovw-search", methods=["POST"])
def bovw(): 
    if request.method == "POST": 
        filestr = request.files["img"].read()
        RESULTS_ARRAY = bovw_search(filestr)
        results_bovw = RESULTS_ARRAY
        return jsonify(results=RESULTS_ARRAY)



@app.route("/cnn-search", methods=["POST"])
def cnn():
    if request.method == "POST":
        filestr = request.files["img"].read()
        RESULTS_ARRAY =  cnn_search(filestr)
        results_cnn = RESULTS_ARRAY
        return jsonify(results=RESULTS_ARRAY)


    

#====== INDEX =========#
@app.route("/all-index", methods=["POST"])
def all_index():
    if request.method == "POST":
        try: 
            images = request.files

            (img_paths, img_names) = save_imgs(images)
            
            if img_paths and img_names: 
                # Currentyl saving with every call. Might change later.
                print(Fore.GREEN + "Indexing for color algorithm")
                _basic_index(img_paths, img_names)        
                print(Fore.GREEN + "Done indexing for color algorithm")
                print(Fore.GREEN + "Indexing for cnn algorithm")
                _cnn_index(img_paths, img_names)
                print(Fore.GREEN + "Done indexing for cnn algorithm")
                #_bovw_index(images)

                print(Back.RESET + Fore.RESET)
                return jsonify(message="Files indexed successfully.")
            else: 
                return jsonify(message="Files already indexed.")
        
        except Exception as e:
            print(e)
            return jsonify(message="Something went wrong.")
        
# filestr is array of image strings
def _cnn_index(img_paths, img_names):
    try: 
        if os.path.isdir(VGG16_CNN):
            model = keras.models.load_model(VGG16_CNN)
            print("Loading local vgg16")
        else:
            model = VGG16(weights="imagenet", include_top=False)
            print("Downloading vgg16")
        index_file = open(INDEX_CNN, "a")

        for i in range(len(img_paths)):
            img = image.loag_img(img_paths[i], target_size(244, 244))
            
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            features = model.predict(img_array)
            features_numpy = np.array(features)

            #save file to static/images

            write_to_index(features_numpy.flatten(), img_name, index_file)

        index_file.close()
        return
    except Exception as e: print(e)


def _bovw_index(img_paths, img_names):
    try:
        
        if os.path.isfile(CLUSTER):
            clusters = load(CLUSTER)
        else:
            return jsonify({"message": "Didn't findt local clusters"}, 500);

        index_file = open(INDEX_BOVW, "a")
        histogramBuilder = HistogramBuilder()
        siftDescriptor = SiftDescriptor(200)

        for i in range(len(img_paths)):
            img_name = img_names[i]
            img_path = img_paths[i]
            index_img_grayscale = cv2.imread(img_path, 0)

            descriptors = siftDescriptor.describe(index_img_grayscale) 
            index_histogram = histogramBuilder.compute_histogram(descriptors, clusters)

            #save file to static/images

            write_to_index(index_histogram, img_name, index_file)

        index_file.close()
        return
    except Exception as e: print(e)
        
def _basic_index(img_paths, img_names):
    try:
        index_file = open(INDEX_SIMPLE, "a") 
        colorDescriptor = ColorDescriptor((8, 12, 3))
        for i in range(len(img_paths)):
            img = cv2.imread(img_paths[i])
            img_name = img_names[i]
            
            features = colorDescriptor.describe(img)
            features_array = np.array(features)

            write_to_index(features_array, img_name, index_file)

        index_file.close()
        return

    except Exception as e: print(e)
    

#==== ROCCHIO ====#


@app.route("/all-rocchio", methods=["POST"])
def rocchio():
    if request.method == "POST":

        data = request.json

        relevant_basic = data["relevant_basic"]
        nonrelevant_basic = data["nonrelevant_basic"]
        relevant_bovw = data["relevant_bovw"]
        nonrelevant_bovw = data["nonrelevant_bovw"]
        relevant_cnn = data["relevant_cnn"]
        nonrelevant_cnn = data["nonrelevant_cnn"]

        
        basic_query = _basic_rocchio(relevant_basic, nonrelevant_basic)
        bovw_query = _bovw_rocchio(relevant_basic, nonrelevant_basic)
        cnn_query = _cnn_rocchio(relevant_basic, nonrelevant_basic)

        
        
        print("searching_again")
        return _all_search(basic_query, bovw_query, cnn_query)
        

def _basic_rocchio(relevant_imgs, nonrelevant_imgs, a=1, b=0.75, c=0.15):
    relevant_features = load_features(relevant_imgs, INDEX_SIMPLE)
    nonrelevant_features = load_features(nonrelevant_imgs, INDEX_SIMPLE)

    global curr_query_simple
    query_array = np.array(curr_query_simple)
    
    query_part = query_array * a
    
    sum_relevant = sum_vectors(relevant_features)
    relevant_part = b * (1 / len(relevant_features)) * sum_relevant

    sum_nonrelevant = sum_vectors(nonrelevant_features)
    nonrelevant_part = c * (1 / len(nonrelevant_features)) * sum_nonrelevant

    new_query = np.subtract(np.add(query_part, relevant_part), nonrelevant_part)
    return new_query


def _cnn_rocchio(relevant_imgs, nonrelevant_imgs, a=1, b=0.75, c=0.15):
    relevant_features = load_features(relevant_imgs, INDEX_CNN)
    nonrelevant_features = load_features(nonrelevant_imgs, INDEX_CNN)

    global curr_query_cnn
    query_array = np.array(curr_query_cnn)
    
    query_part = query_array * a
    
    sum_relevant = sum_vectors(relevant_features)
    relevant_part = b * (1 / len(relevant_features)) * sum_relevant

    sum_nonrelevant = sum_vectors(nonrelevant_features)
    nonrelevant_part = c * (1 / len(nonrelevant_features)) * sum_nonrelevant

    new_query = np.subtract(np.add(query_part, relevant_part), nonrelevant_part)
    return new_query


def _bovw_rocchio(relevant_imgs, nonrelevant_imgs, a=1, b=0.75, c=0.15):
    relevant_features = load_features(relevant_imgs, INDEX_BOVW)
    nonrelevant_features = load_features(nonrelevant_imgs, INDEX_BOVW)

    global curr_query_bovw
    query_array = np.array(curr_query_bovw)
    
    query_part = query_array * a
    
    sum_relevant = sum_vectors(relevant_features)
    relevant_part = b * (1 / len(relevant_features)) * sum_relevant

    sum_nonrelevant = sum_vectors(nonrelevant_features)
    nonrelevant_part = c * (1 / len(nonrelevant_features)) * sum_nonrelevant

    new_query = np.subtract(np.add(query_part, relevant_part), nonrelevant_part)
    return new_query



#==== SEARCH ====#
    
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

        global curr_query_cnn
        curr_query_cnn = features_numpy.flatten()

        (dist, img_ids) = searcher.search(curr_query_cnn, 10)


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
        siftDescriptor = SiftDescriptor(200)
        histogramBuilder = HistogramBuilder()
        searcher = SearcherBovw(INDEX_BOVW)

        # Load querry image and describe it
        import cv2

        npimg = np.frombuffer(filestr, np.uint8)
        # Query image is already in BGR
        query_image = cv2.imdecode(npimg, -1)
        query_image_grayscale = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
        descriptors = siftDescriptor.describe(query_image_grayscale)
        kmeans = load(CLUSTER)
        query_histogram = histogramBuilder.compute_histogram(descriptors, kmeans)

    

        global curr_query_bovw
        curr_query_bovw = query_histogram
        


        (distance, image_idxs) = searcher.search(query_histogram, 10)


        # Loop over the results and displaying score and image name
        # for i in range(len(image_ids)):
        #     RESULTS_ARRAY.append(
        #         {"image": str(image_ids[i]), "score": str(distances[i])}
        #         )

        img_ids = get_ids(image_idxs, INDEX_BOVW)

        
        for i in range(len(img_ids)):
            RESULTS_ARRAY.append(
                {"image": str(img_ids[i]), "score": str(distance[0][i])}
                )

        print(RESULTS_ARRAY[:10])
            
        return RESULTS_ARRAY[:10]

    except Exception as e:
        print(e)

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
        global curr_query_simple
        curr_query_simple = features


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

#==== SEARCH FUNCTIONS QUERY INPUT ====#

def basic_search_query(query_features):
    RESULTS_ARRAY = []

    try:
        global curr_query_simple
        curr_query_simple = query_features

        # Perform search
        searcher = SearcherSimple(INDEX_SIMPLE)
        results  = searcher.search(query_features)

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



def bovw_search_query(query_features): 
    RESULTS_ARRAY = []
    try:
        searcher = SearcherBovw(INDEX_BOVW)

        # Load querry image and describe it
        import cv2

        global curr_query_bovw
        curr_query_bovw = query_features
        


        (distances, img_idxs) = searcher.search(query_features, 10)
        img_ids = get_ids(img_idxs, INDEX_BOVW)
        
        for i in range(len(img_ids)):
            RESULTS_ARRAY.append(
                {"image": str(img_ids[i]), "score": str(distances[0][i])}
                )

        

        return RESULTS_ARRAY[:10]

    except Exception as inst:
        print(inst)

        # Return error
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


def cnn_search_query(query_features): 
    RESULTS_ARRAY = []
    try:
        searcher = SearcherCNN(INDEX_CNN)

        import cv2

        global curr_query_cnn
        curr_query_cnn = query_features

        (dist, img_ids) = searcher.search(curr_query_cnn, 10)


        for i in range(len(img_ids)):
            RESULTS_ARRAY.append(
                {"image": str(img_ids[i]), "score": str(dist[i])}
                )
            

        return RESULTS_ARRAY[:10]
    except:
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500            



    
#==== HELPER FUNCTIONS ====#    
    
def write_to_index(features, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(features.astype(str))))

def check_if_img_exists(img_path):
    return os.path.isfile(img_path)
    
def save_imgs(imgs):
    img_paths = []
    img_names = []
    
    for key in imgs:
        img = imgs[key]
        file_exists = check_if_img_exists(os.path.join(STATIC, img.filename))
        
        if not file_exists:
            (img_path, img_name) = save_img(img)
            img_paths.append(img_path)
            img_names.append(img_name)

    return img_paths, img_names
        
        
def save_img(img):
    img_path = os.path.join(STATIC, img.filename)
    print(Fore.BLUE + "Saving img")
    print(img_path)
    img.save(os.path.join(STATIC, img.filename))
    print(Fore.RESET)
    return img_path, img.filename

    


def load_features(img_ids, index_path):
    n_vectors = len(img_ids)
    features = []

    with open(index_path, mode="r") as index_file:
        csv_reader = csv.reader(index_file, delimiter=",")

        vector_count = 0
        for row in csv_reader:
            for img_id in img_ids:
                if row[0] == img_id: 
                    feature_vector = row[1:]
                    features.append(feature_vector)
                    vector_count += 1

                if vector_count == n_vectors:
                    return np.array(features).astype(np.float)

def sum_vectors(vectors):
    _sum = np.array(vectors[0])
    for i in range(1, len(vectors)):
        _sum = np.add(_sum, vectors[i])
    return _sum
        
def get_ids(image_idxs, index):

    with open(index) as index_file:
        reader = csv.reader(index_file)

        ids = []

        for row in reader:
            ids.append(row[0])


        image_ids = []
        for image_idx in image_idxs[0]:
            image_ids.append(ids[image_idx])

        return image_ids
                
# Run!
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
