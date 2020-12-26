import cv2


# Extracts features with sift
class SiftDescriptor:
    def describe(self, image):
        #print("Sift descritpor running")
        sift = cv2.SIFT_create()

        keypoints, descriptors = sift.detectAndCompute(image, None) 

        descriptors = descriptors.astype(float)
        #print("Sift descritpor finished")
        return descriptors
