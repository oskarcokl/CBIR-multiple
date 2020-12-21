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
