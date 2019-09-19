from streak_image import StreakImage
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", action="store_true", default=False, help="Verbose mode."
)
parser.add_argument(
    "-p", "--plot", action="store_true", default=False, help="plot Data"
)

args = parser.parse_args()
verbose = args.verbose
plot = args.plot

test = StreakImage("test/test_file2.img", verbose)
if plot:
    data = test.data
    plt.pcolormesh(data)
    plt.show()

# print(test.height)
