import os
import numpy as np
#from image_loader import ImageLoader
from sklearn.neighbors import NearestNeighbors
import csv


class Searcher:
    def __init__(self, indexPath):
        # Store index path
        self.indexPath = indexPath


    def cosine_similarity(self, A, B):
        dot = np.dot(A, B)
        lenA = np.linalg.norm(A)
        lenB = np.linalg.norm(B)
        return (dot) / (lenA * lenB)
    
    def search(self, query_histogram, neighbors):
        results = {}
        histograms = []
        image_ids_all = []

        with open(self.indexPath) as indexFile:
            reader = csv.reader(indexFile)
            
            for row in reader:
                histogram = [float(x) for x in row[1:]]
                image_ids_all.append(row[0])
                histograms.append(histogram)
                #dist = self.cosine_similarity(query_histogram, histogram)
                #results[row[0]] = dist

                                         

                

            neighborModel = NearestNeighbors(n_neighbors = neighbors)
            neighborModel.fit(histograms)

            (dist, results) = neighborModel.kneighbors([query_histogram])
            

                
        indexFile.close()

        # results = sorted([(v, k) for (k, v) in results.items()])

        # breakpoint()
        
        return dist, results
 
        # image_ids = []


        # for result in results[0]:
        #     image_ids.append(image_ids_all[result])

        # return dist[0], image_ids

             
