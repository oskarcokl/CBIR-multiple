from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

# Parse arguments
argsParser = argparse.ArgumentParser()
argsParser.add_argument("-d", "--dataset", required=True,
    help="Path to directory that contains the images to be indexed")
argsParser.add_argument("-i", "--index", required=True,
    help="Path to where teh computed idnex will be stored")
args = vars(argsParser.parse_args())

colorDescriptor = ColorDescriptor((8, 12, 3))
