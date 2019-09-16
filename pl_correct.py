# import argparse
# from streak_image import StreakImage
# from load_file

# parser = argparse.ArgumentParser()

# parser.add_argument(
#     "files",
#     action="store",
#     type=list,
#     help="list containing one or multiple files to convert",
# )
# parser.add_argument(
#     "-bg", "background", action="store", type=StreakImage, help="subtract background"
# )

# args = parser.parse_args()

# file_list = args.files
# subtract_bg = args.bg

# def __main__():
#     for file_path in file_list:
#         file = StreakImage(file_path)

#         if subtract_bg:
#             file.subtract_bg()

# if __name__ == "__main__":
#     __main__()
