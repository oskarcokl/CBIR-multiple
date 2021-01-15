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
                           
    args = vars(argParser.parse_args())


 
    # Image dataset
    dataset_folder_path = args["dataset"]
    
    n_images = len([name for name in os.listdir(dataset_folder_path) if os.path.isfile(os.path.join(dataset_folder_path, name))])


    imageLoader = ImageLoader()
    siftDescriptor = SiftDescriptor()

    descriptor_list = []
    descriptor_array = []
    n_clusters = int(args["clusters"])

    if args["training"] == "train":


        # Reading images and getting their descriptors
        i = 1;
        for imageID in os.listdir(dataset_folder_path):
            full_path_to_image = dataset_folder_path + imageID
            image = cv2.imread(full_path_to_image)
            image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            descriptor = siftDescriptor.describe(image)
            descriptor_list.append(descriptor)
            #descriptor_array.append(descriptor)
            print(i, "out of", n_images)
            i += 1


        
        # Getting clusters from the descriptor_list
        myKMeans = MyKMeans()
        print("Running k_means")

        
        print(len(descriptor_list[1:]))
        print("Vstacking over")
        vstack_descriptor = vstack_descriptors(descriptor_list)
        print("Vstacking over")


        
        clusters = myKMeans.k_means_batch(n_clusters, vstack_descriptor, 200)
        print("Finished k_means")

        dump(clusters, "train_k_means.joblib")
    else:

        # Open the indexFile in which we will save the indexed images
        indexFile = open(args["index"], "w")
        clusters = load("train_k_means.joblib")
        
        histogramBuilder = HistogramBuilder()


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


        features_list = extract_features(clusters, descriptor_list, n_images, n_clusters)


        scale = StandardScaler().fit(features_list)
        features_list = scale.transform(features_list)
        
        print(features_list.shape)

        index = 0
        for feature in features_list:
            write_to_index(feature, image_ids[index], indexFile)
            index+=1
        
        
        indexFile.close()
        print("Finished")



def write_to_index(histogram, imageID, indexFile):
    indexFile.write("%s,%s\n" % (imageID, ",".join(histogram.astype(str))))


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



index()
