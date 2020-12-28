import os
import numpy as np
from .image_loader import ImageLoader
from sklearn.neighbors import NearestNeighbors
import csv


class Searcher:
    def __init__(self, indexPath):
        # Store index path
        self.indexPath = indexPath
    
    def search(self, queryHistogram, neighbors):
        results = {}
        histograms = []
        image_ids_all = []

        with open(self.indexPath) as indexFile:
            reader = csv.reader(indexFile)
            
            for row in reader:
                histogram = [float(x) for x in row[1:]]
                image_ids_all.append(row[0])
                histograms.append(histogram)


            print(len(histograms))
                

            neighborModel = NearestNeighbors(n_neighbors = neighbors)
            neighborModel.fit(histograms)

            dist, results = neighborModel.kneighbors([queryHistogram])

                
        indexFile.close()
 
        image_ids = []


        for result in results[0]:
            image_ids.append(image_ids_all[result])

        return dist[0], image_ids
