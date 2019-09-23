from streak_image import StreakImage
import argparse
import matplotlib.pyplot as plt
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("file", action="store", default="test", help="file to plot")
parser.add_argument(
    "-v", "--verbose", action="store_true", default=False, help="Verbose mode."
)
parser.add_argument(
    "-p", "--plot", action="store_true", default=False, help="plot data"
)

args = parser.parse_args()
verbose = args.verbose
plot = args.plot
file = args.file

data: np.ndarray = None

if file == "test":
    image = StreakImage("../test/test_file2.img", verbose)
    data = image.data
elif os.path.isfile(file):
    image = StreakImage(file, verbose)
    data = image.data

if plot and data != None:
    plt.pcolormesh(data)
    plt.show()

# print(test.height)
