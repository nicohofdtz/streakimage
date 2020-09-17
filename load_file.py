from pl_py import StreakImage
import argparse
import matplotlib.pyplot as plt
import os
import numpy as np
from json_tricks import loads as jt_loads

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store", default="", help="file to plot")
parser.add_argument(
    "-v", "--verbose", action="store_true", default=False, help="Verbose mode."
)
parser.add_argument(
    "-p", "--plot", action="store_true", default=False, help="plot data"
)
parser.add_argument(
    "-t", "--test", action="store_true", default=False, help="Test mode."
)

args = parser.parse_args()
file = args.file
verbose = args.verbose
plot = args.plot
test = args.test

image: StreakImage
data: np.ndarray = None

if test:
    file = "test/calib_files/100.img"
if os.path.isfile(file):
    image = StreakImage(file, verbose, correction=True)
    # data = image.data
    if plot and data is not None:
        plt.pcolormesh(data)
        plt.show()

    # print(image.get_date())
    # json = jt_loads(image.get_json())
    # del json[data]
    # print((image.get_json()))
else:
    print("File not found")
