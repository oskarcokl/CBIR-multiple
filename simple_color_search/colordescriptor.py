import numpy as np
import cv2
import imutils

class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        # Convert image to hsv
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Prepearing features array
        features = []

        #Dimesnsion of image
        (h, w) = image.shape[:2] # same as [0:2]
        (cX, cY) = (int(w / 2), int(h / 2))