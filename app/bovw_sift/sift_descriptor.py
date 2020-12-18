import cv2


# Extracts features with sift
class SiftDescriptor:

	def describe(images):
		sift_vectors = []
		descriptor_list = []
		sift = cv2.xfeatures2d.SIFT_create()

		for image in images:
			keypoints, descriptors = sift.detectAndCompute()	