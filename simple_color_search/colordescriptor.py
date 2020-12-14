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

        # Dimesnsion of image
        (h, w) = image.shape[:2] # same as [0:2]
        (cX, cY) = (int(w / 2), int(h / 2))

        # Dividing image into 4 rectangle segments (top-left, top-right
        # bottom-left bottom-right)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

        # Eliptical mask for the center of the screen
        (axesX, axesY) = (int(w *0.75) // 2, int(h * 0.75) // 2)        
        # Mask is just a black image (that's why we use the zeros)
        ellipsMask = np.zeros(image.shape[:2], dtype="unit8")
        cv2.ellipse(ellipsMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # Loop over segments
        for (startX, endX, startY, endY) in segments:
            # Construct mask for each corner by subracting elipse
            # from the square
            cornerMask = np.zeros(image.shape[:2], dtype="unit8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipsMask)

            # Extrect color histogram and update the features vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        # Can't forget to also extract the color histogram from the center elipse
        hist = self.histogram(image, ellipsMask)
        features.extend(hist)

        return features

    def histogram(self, image, mask):
        # Extract a 3D color histogram from mask region of the image
        hist = cv2.calcHist([image], [0, 1, 2], self.bins, [0, 180, 0, 256, 0, 256])

        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        else:
            hist = cv2.normalize(hist, hist).flatten()

        return hist