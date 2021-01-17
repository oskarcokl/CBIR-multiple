from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import numpy as np


class HistogramBuilder: 
    def build_histogram_from_clusters(self, descriptor, clusters):
        histogram = np.zeros(len(clusters.cluster_centers_))
        cluster_result = clusters.predict(descriptor)
        for i in cluster_result:
                histogram[i] += 1.0
        return histogram
    
    def build_all_histograms(self, descriptors, clusters):
        histograms = []

        for descritpor in descriptors:
            histogram = build_histogram(descritpor, clusters)

            histograms.append(histogram)

        return histograms


    def compute_histogram(self, descriptors, k_means):
        histogram = np.zeros(len(k_means.cluster_centers_))
        predictions = k_means.predict(descriptors)
        for prediction in predictions:
            histogram[prediction] += 1
        return histogram

    def compute_histograms(self, descriptors_list, k_means):
        histograms = []
        for descriptors in descriptors_list:
            histogram = compute_histogram(descriptors, k_means)
            histograms.append(histogram)
        return histograms
