from streak_image import StreakImage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", action="store_true", default=False, help="Verbose mode."
)

args = parser.parse_args()
verbose = args.verbose

test = StreakImage("test/test_file2.img", verbose)
# print(test.height)
