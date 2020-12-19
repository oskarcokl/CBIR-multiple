import numpy as np
from shutil import copy
import glob
from sklearn.model_selection import train_test_split

folder = "..\\..\\data"



def split_dataset(folder):
	images = []

	for imagePath in glob.glob(folder + "/*.jpg"):
		images.append(imagePath)

	images_train, images_test = train_test_split(images, test_size=0.2)

	for image in images_train:
		print("Copying ", image)
		dst = "../../data/train"
		copy(image, dst)

	for image in images_test:
		print("Copying ", image)
		dst = "../../data/test"
		copy(image, dst)

#split_dataset(folder)

print("hello")
