from image_loader import ImageLoader
import numpy as np
from sift_descriptor import SiftDescriptor
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
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
    args = vars(argParser.parse_args())


 
    # Image dataset
    dataset_folder_path = args["dataset"]
    
    n_images = len([name for name in os.listdir(dataset_folder_path) if os.path.isfile(os.path.join(dataset_folder_path, name))])


    imageLoader = ImageLoader()
    siftDescriptor = SiftDescriptor()

    descriptor_list = []
    descriptor_array = []

    if args["training"] == "train":


        # Reading images and getting their descriptors
        i = 1;
        for imageID in os.listdir(dataset_folder_path):
            full_path_to_image = dataset_folder_path + imageID
            image = cv2.imread(full_path_to_image)
            image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            descriptor = siftDescriptor.describe(image)
            descriptor_list.extend(descriptor)
            descriptor_array.append(descriptor)
            print(i, "out of", n_images)
            i += 1


        
        # Getting clusters from the descriptor_list
        myKMeans = MyKMeans()
        print("Running k_means")
        clusters = myKMeans.k_means_batch(10000, descriptor_list, 100)
        print("Finished k_means")

        dump(clusters, "train_k_means.joblib")
    else:

        # Open the indexFile in which we will save the indexed images
        indexFile = open(args["index"], "w")
        clusters = load("train_k_means.joblib")
        
        histogramBuilder = HistogramBuilder()


        # Reading images and getting their descriptors
        i = 1;
        print("Building histograms")
        for imageID in os.listdir(dataset_folder_path):
            full_path_to_image = dataset_folder_path + imageID
            image = cv2.imread(full_path_to_image)
            image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            descriptor = siftDescriptor.describe(image)
            
            histogram = histogramBuilder.build_histogram_from_clusters(descriptor, clusters)

            
            print("Writing to index file")
            write_to_index(histogram, imageID, indexFile)
            print("Finished writing to index file")
    
            print(i, "out of", n_images)
            i += 1
        indexFile.close()
        print("Finished")



def write_to_index(histogram, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(histogram.astype(str))))
 

index()
