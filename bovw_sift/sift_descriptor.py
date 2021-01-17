import cv2


# Extracts features with sift
class SiftDescriptor:
    def __init__(self, n):
        print("Creating sift descriptor with", n, "of features.")
        self.sift = cv2.SIFT_create(nfeatures=n)
        #print(self.sift.getDefaultName())
        print("Done creating sift descriptor")
    

    def describe(self, image):
        keypoints, descriptors = self.sift.detectAndCompute(image, None) 
        descriptors = descriptors.astype(float)
        return descriptors
