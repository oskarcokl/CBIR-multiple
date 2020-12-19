import cv2


# Extracts features with sift
class SiftDescriptor:
    def describe(self, images):
        print("Sift descritpor running")
        sift_vectors = []
        descriptor_list = []
        sift = cv2.SIFT_create()
        
        for image in images:
            keypoints, descriptors = sift.detectAndCompute(image, None) 
            descriptor_list.extend(descriptors)
            sift_vectors.append(descriptors)
            

        print("Sift descritpor finished")
        return descriptor_list, sift_vectors

