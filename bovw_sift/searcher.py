import os
import numpy as np
from image_loader import ImageLoader
from sklearn.neighbors import NearestNeighbors
import csv


class Searcher:
    def __init__(self, indexPath):
        # Store index path
        self.indexPath = indexPath
    
    def search(self, queryHistogram, neighbors):
        results = {}
        histograms = []

        with open(self.indexPath) as indexFile:
            reader = csv.reader(indexFile)
            
            for row in reader:
                histogram = [float(x) for x in row[1:]]
                histograms.append(histogram)

             

            neighborModel = NearestNeighbors(n_neighbors = neighbors)
            neighborModel
            neighborModel.fit(histograms)

            dist, results = neighborModel.kneighbors([queryHistogram])

            image_ids_all = [row[0] for row in csv.reader(index)]

                
        indexFile.close()
 
        image_ids = []

        for result in results[0]:
            image_ids.push(image_ids_all[result])

        return dist, image_ids
