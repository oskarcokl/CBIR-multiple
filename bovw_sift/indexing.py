from image_loader import ImageLoader
import numpy as np
from sift_descriptor import SiftDescriptor
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from k_means import MyKMeans
from histogram_builder import HistogramBuilder
from joblib import dump, load
import argparse
import glob
import os
import cv2

def index():

    # Parse arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-d", "--dataset", required=True,
        help="Path to directory that contains the images to be indexed")
    argParser.add_argument("-i", "--index", 
        help="Path to where teh computed idnex will be stored")
    argParser.add_argument("-t", "--training", action="store_const", const="train",
                           help="If you want to jus train the knn model no csv file will be created")
    argParser.add_argument("-c", "--clusters", default=50,
                           help="Number of clusters for the k_means model.")
    argParser.add_argument("-f", "--features", default=200,
                           help="Number of features for the sift descriptor.")
                           
    args = vars(argParser.parse_args())


 
    # Image dataset
    dataset_folder_path = args["dataset"]
    
    n_images = len([name for name in os.listdir(dataset_folder_path) if os.path.isfile(os.path.join(dataset_folder_path, name))])


    n_features = int(args["features"])
    imageLoader = ImageLoader()
    siftDescriptor = SiftDescriptor(n_features)

    descriptor_list = []
    descriptor_array = []
    n_clusters = int(args["clusters"])

    if args["training"] == "train":

        try:
            # Reading images and getting their descriptors
            i = 1;
            for imageID in os.listdir(dataset_folder_path):
                full_path_to_image = dataset_folder_path + imageID
                image = cv2.imread(full_path_to_image)
                image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                #print("Describing")
                descriptor = siftDescriptor.describe(image)
                #breakpoint()
                #print("Done")            

                descriptor_list.extend(descriptor)
                #descriptor_array.append(descriptor)
                #print(i, "out of", n_images)
                i += 1



            # Getting clusters from the descriptor_list
            myKMeans = MyKMeans()
            print("Running k_means")


            # print("Vstacking over")
            # vstack_descriptor = vstack_descriptors(descriptor_list)
            # print("Vstacking over")



            clusters = myKMeans.k_means(n_clusters, descriptor_list)

            print(n_clusters)
            print(clusters.inertia_)
            print("Finished k_means")

            dump(clusters, "train_k_means.joblib")
        except Exception as e: print(e)
    else:
        try:
            # Open the indexFile in which we will save the indexed images
            indexFile = open(args["index"], "w")
            clusters = load("train_k_means.joblib")

            # Reading images and getting their descriptors
            i = 1;
            descriptor_list = []
            image_ids = []
            print("Building histograms")
            for imageID in os.listdir(dataset_folder_path):
                image_ids.append(imageID)
                full_path_to_image = dataset_folder_path + imageID
                image = cv2.imread(full_path_to_image)
                image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                descriptor = siftDescriptor.describe(image)
                descriptor_list.append(descriptor)
                print(i, "out of", n_images)
                i += 1

            histograms_list = compute_histograms(descriptor_list, clusters)
            
            write_to_index_all(histograms_list, image_ids, indexFile)

            indexFile.close()
            print("Finished")
        except Exception as e: print(e)



def write_to_index(histogram, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(histogram.astype(str))))

def write_to_index_all(histograms_list, img_ids, index_file):
    for i in range(len(histograms_list)):
        write_to_index(histograms_list[i], img_ids[i], index_file)
    return

def vstack_descriptors(descriptor_list):
    i = 0
    print(len(descriptor_list[1:]))
    descriptors = np.array(descriptor_list[0])
    for descriptor in descriptor_list[1:]:
        print(i)
        i+=1
        descriptors = np.vstack((descriptors, descriptor))

    return descriptors

def extract_features(kmeans, descriptor_list, n_images, n_clusters):
    img_features = np.array([np.zeros(n_clusters) for i in range(n_images)])
    for i in range(n_images):
        for j in range(len(descriptor_list[i])):
            feature = descriptor_list[i][j]
            feature = feature.reshape(1, 128)
            idx = kmeans.predict(feature)
            img_features[i][idx] += 1

    return img_features

def compute_histogram(descriptors, k_means):
    histogram = np.zeros(len(k_means.cluster_centers_))
    predictions = k_means.predict(descriptors)
    for prediction in predictions:
        histogram[prediction] += 1
    return histogram

def compute_histograms(descriptors_list, k_means):
    histograms = []
    for descriptors in descriptors_list:
        histogram = compute_histogram(descriptors, k_means)
        histograms.append(histogram)
    return histograms
        


index()
