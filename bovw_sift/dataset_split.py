import numpy as np
import shutil
import glob
import argparse
import os

from sklearn.model_selection import train_test_split



def split_dataset():
        argParser = argparse.ArgumentParser()
        argParser.add_argument("-s", "--source", required=True,
                               help="Path to directory that contains images you want to copy.")
        argParser.add_argument("-d", "--destination", required=True,
                               help="Directory to which the images will be coppied.")
        argParser.add_argument("-n", "--number", required=True,
                               help="Number of images to copy from each directory.")
        args = vars(argParser.parse_args())

        


        src = args["source"]
        dst = args["destination"]
        n_images = args["number"]

        with os.scandir(src) as entries:
                for entry in entries:
                        path = os.path.join(src, entry.name)
                        with os.scandir(path) as images:
                                i = 0
                                for image in images:
                                        if (i <= int(n_images)):
                                                shutil.copy(os.path.join(path, image.name), dst)
                                                i += 1
                                        else:
                                                break
        
        
        

split_dataset()
