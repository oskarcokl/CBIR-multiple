from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

# Parse arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--dataset", required=True,
    help="Path to directory that contains the images to be indexed")
argParser.add_argument("-i", "--index", required=True,
    help="Path to where teh computed idnex will be stored")
args = vars(argParser.parse_args())

# 8 hue bins, 12 saturation bins, 3 value bins
colorDescriptor = ColorDescriptor((8, 12, 3))

# Open the indexFile in which we will save the indexed images
indexFile = open(args["index"], "w")

# Loop over image files with glob
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    imageID = imagePath[imagePath.rfind("\\") + 1:]
    image = cv2.imread(imagePath)

    breakpoint()

    # get the features 
    features = colorDescriptor.describe(image)


    # write feature to file
    features = [str(f) for f in features]
    indexFile.write("%s,%s\n" % (imageID, ",".join(features)))

indexFile.close()
