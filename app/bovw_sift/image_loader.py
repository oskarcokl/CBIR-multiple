import os
import cv2

class ImageLoader:
	def load_images_from_folder(self, folder):	
		images = [] 
		for imageID in os.listdir(folder):
			fullPathToImage = folder + imageID
			print(fullPathToImage)
			loadedImage = cv2.imread(fullPathToImage)

			images.append({
				"imageID": imageID,
				"imagePath": fullPathToImage,
				"image": loadedImage
				})

		return images

	def load_images_from_folder_and_grayscale(self, folder):	
		images = []

		for imageID in os.listdir(folder):
			fullPathToImage = folder + imageID
			print(fullPathToImage)
			loadedImage = cv2.imread(fullPathToImage)
			grayScaledImage = cv2.cvtColor(loadedImage, cv2.COLOR_BGR2GRAY)

			images.append({
				"imageID": imageID,
				"imagePath": fullPathToImage,
				"image": grayScaledImage
				})

		return images
