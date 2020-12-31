import os
import numpy as np
from .image_loader import ImageLoader
from sklearn.neighbors import NearestNeighbors
import csv


class Searcher:
    def __init__(self, indexPath):
        # Store index path
        self.indexPath = indexPath
    
    def search(self, query_histogram, limit):
        results = {}
        histograms = []
        image_ids_all = []

        with open(self.indexPath) as indexFile:
            reader = csv.reader(indexFile)
            
            for row in reader:
                histogram = [float(x) for x in row[1:]]
                #image_ids_all.append(row[0])
                #histograms.append(histogram)
                distnace = self.cosine_similarity(histogram, query_histogram)
                results[row[0]] = distance


            #print(len(histograms))
                

            # neighborModel = NearestNeighbors(n_neighbors = neighbors)
            # neighborModel.fit(histograms)

            # dist, results = neighborModel.kneighbors([queryHistogram])
        indexFile.close()
 


        # for result in results[0]:
        #     image_ids.append(image_ids_all[result])

        results = sorted([(v, k) for (k, v) in results.items()])
        
        return results[:limit]

    def cosine_similarity(A, B):
        dot = np.dot(A, B)
        lenA = np.linalg.norm(A)
        lenB = np.linalg.norm(B)
        return (dot) / (lenA * lenB)

    def calculate_distance(histograms, ids):
        
