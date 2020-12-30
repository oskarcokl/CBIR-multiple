import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
import csv

class Searcher:
    def __init__(self, index_path):
        self.index_path = index_path

def search(self, query_features, neighbors):
    results = {}
    feature_list = []
    img_ids_all = []


    with open(self.index_path) as index_file:
        reader = csv.reader(index_file)

        for row in reader:
            feature = [float(x) for x in row[1:]]
            img_ids_all.append(row[0])
            feature_list.append(feature)

        feature_array = np.array(feature_list)
            
        neighbor_model = NearestNeighbors(n_neighbors = neighbors)
        neighbor_model.fit(feature_array)

        dist, results = neighbor_model.kneighbors([qurey_features])


    index_file.close()
    img_ids = []

    for result in results[0]:
        img_ids.append(img_ids_all[result])

    return dist[0], img_ids
