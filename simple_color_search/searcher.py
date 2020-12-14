import numpy as np
import csv

class Searcher:
    def __init__(self, indexPath):
        # Store index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit = 10):
        # Intialize dictionary of result
        results = {}

        # Open index file for searching
        with open(self.indexPath) as indexFile:
            reader = csv.reader(indexFile)

        # Loop over the rows in the indexFile
        for row in reader:
            # Calculating chi-square distance between features in index 
            # and features in querry image
            features = [float(x) for x in row[1:]]
            distance = self.chi2_distance(features, queryFeatures)

            # They key is the image ID
            results[row[0]] = distance

        indexFile.close()

        # Sort the result so that the "more similar images" are at
        # the top of the dictionary
        results = sorted([(v, k) for (k, v) in results.items()])

        # Return only the top "limit" results
        return results[:limit]


    def chi2_distance(self, histA, histB, eps = 1e-10):
        distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])

        return distance