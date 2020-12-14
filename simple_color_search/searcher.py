import numpy as np
import csv

class Searcher:
    def __init__(self, indexPath):
        # store index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit = 10):
        # intialize dictionary of result
        results = {}