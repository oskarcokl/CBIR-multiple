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

             
        indexFile.close()

        neighborModel = NearestNeighbors(n_neighbors = neighbors)
        neighborModel
        neighborModel.fit(histograms)

        dist, result = neighborModel.kneighbors([queryHistogram])
                
        return dist, result
