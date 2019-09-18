
import argparse
import struct
import numpy

parser = argparse.ArgumentParser()

parser.add_argument("path", action="store", type=str)
args = parser.parse_args()
path = args.path


def main(path):
    # data = numpy.fromfile(path, dtype=">d")
    # print(data)
    # for type in "bBhHiIqQfd":
    #     data = numpy.fromfile(path, dtype=">{:s}".format(type))
    #     print(data)
    file = open(path, "rb")
    file_content = file.read()
    str_data = file_content[100:140].decode()
    print(str_data)


if __name__ == "__main__":
    main(path)
