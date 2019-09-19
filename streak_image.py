import datetime
from datetime import datetime
from enum import Enum
import re
import numpy as np


class FileType(Enum):
    """Enum for the file types used by HPD-TA

    can be 8-bit, 16-bit or compressed
    """

    BIT8 = 0
    COMPRESSED = 1  # not used by HPD-TA
    BIT16 = 2
    BIT32 = 3


class StreakImage:
    """Parses and holds the data of an recorded image

        args:
            file_path: Path to the file to be parsed

    """

    def __init__(self, file_path: str, verbose: bool = False):
        self.date: datetime
        self.comment_length: int
        self.width: int
        self.height: int
        self.x_offset: int
        self.y_offset: int
        self.file_type: FileType
        self.data: np.array[np.array]
        self.comment_string: str
        self.parameters: dict
        self.verbose: bool = verbose

        self.parse_file(file_path)
        # print("Date:", self.date)
        if self.verbose:
            print("Comment length:", self.comment_length)
            print("Width:", self.width, "Height:", self.height)
            print("x-offset:", self.x_offset, "y-offset", self.y_offset)
            print("file-type:", self.file_type.name)
            print("comment:", self.comment_string)

    def parse_file(self, file_path: str):
        """Read the given file and parse the content to class fields.

        args:
            file_path: Path to the file to be parsed

        """
        with open(file_path, "rb") as file:
            file_content = file.read()
            self.im_chars = file_content[0:2].decode("utf-8")
            self.comment_length = int.from_bytes(
                file_content[2:4], byteorder="little", signed=False
            )
            self.width = int.from_bytes(
                file_content[4:6], byteorder="little", signed=False
            )
            self.height = int.from_bytes(
                file_content[6:8], byteorder="little", signed=False
            )
            self.x_offset = int.from_bytes(
                file_content[8:9], byteorder="little", signed=False
            )
            self.y_offset = int.from_bytes(
                file_content[10:11], byteorder="little", signed=False
            )
            file_type_int = int.from_bytes(
                file_content[12:13], byteorder="little", signed=False
            )
            self.file_type = FileType(file_type_int)
            nnn = 64 + self.comment_length
            self.comment_string = file_content[64:nnn].decode("utf-8")
            # self.parameters =
            # print(self.comment_string)
            self.parse_comment(self.comment_string)
            self.data = self.parse_data(file_content[nnn:])

    def parse_data(self, binary_data: bytes):
        """Parse given data bytes to 2d list

        args:
            binary_data: The part of the file containing the intensity data.

        """
        data = np.zeros((self.height, self.width))
        byte_per_pixel = 2 if self.file_type == FileType.BIT16 else 4
        from_ = 0
        to = byte_per_pixel

        for wl in range(0, self.height):
            for time in range(0, self.width):
                data[wl][time] = int.from_bytes(
                    binary_data[from_:to], byteorder="little", signed=False
                )
                from_ += byte_per_pixel
                to += byte_per_pixel
        with open("data.txt", "w") as file:
            for line in data:
                # file.writelines(str(line)[1:-1] + "\n")
                for num in line:
                    file.write(str(num) + "\t")
                file.write("\n")
        return data

    def parse_comment(self, comment: str) -> dict:
        """Parse the comment string and return it as a dictionary

        The argument hast to be a 

        args:
            comment: the comment string

        return:
            The returned object is a dictionary of dictionaries. The first level is a dictionary of the comment categories. 
            The second level dictionaries contain the key-value pairs of each category. 

        """
        # build 1st level dictionary
        comment_dict: dict = {}
        # split comment string into category substrings
        comment_list: list = comment.split(sep="\r\n")

        # last entry needs special treatment due to missing line break
        if comment_list[-1].find("[Comment]") > 0:
            corrected_list = re.split("(\[Comment\],.*)", comment_list[-1])
            comment_list[-1] = corrected_list[0]
            comment_list.append(corrected_list[1])

        # build 2nd level dictionaries
        for category in comment_list:
            # category name is written in brackets and is extracted first
            category_name, category_body = re.match(
                "\[(.*?)\]\,(.*)", category
            ).groups()

            key_rex = "[a-zA-Z0-9 ]*"
            value_rex = "[a-zA-Z0-9 ]*"
            quoted_val_rex = '".*?"'
            comma_or_eos_rex = "?:,|$"
            key_val_pair_rex = (
                "("
                + key_rex
                + ")=("
                + value_rex
                + "|"
                + quoted_val_rex
                + ")("
                + comma_or_eos_rex
                + ")"
            )

            category_dict = dict(re.findall(key_val_pair_rex, category_body))

            comment_dict[category_name] = category_dict

        if self.verbose:
            print("Comment parsed. This is the resulting dict:")
            for val in comment_dict:
                print("-" * 60 + "\n")
                print(val + ":")
                print("\n" + "-" * 30)
                for entry in comment_dict[val]:
                    print("\t{:_<22s}:{:s}".format(entry, comment_dict[val][entry]))
                print("\n" + "-" * 30)
            print("-" * 60 + "\n")
        return comment_dict

    def isCompatible(self, other: "StreakImage"):
        """Compare file type and dimension of given classes"""

        if self.height != other.height:
            raise IndexError(
                "Height differs: {:s} vs {:s}".format(self.height, other.height)
            )

        if self.width != other.width:
            raise IndexError(
                "Width differs: {:s} vs {:s}".format(self.width, other.width)
            )

        if self.file_type != other.file_type:
            raise ValueError("File types do not match.")

    def exportSDF(self, path):
        """Export the data to the SDF file format.

        The data is exported to a SDF file at the given path.
        The generated file is compatible to the labview program "PL_Analyze".

        """
        pass
