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



test = "../../data/test/"

imageLoader = ImageLoader()
images = imageLoader.load_images_from_folder(test)
print(images.imageID)