from datetime import datetime, date
from enum import Enum
import re
import numpy as np
import argparse
import json
from json_tricks import dumps as jt_dumps
from collections import OrderedDict
from hpdta8_params import ParaList, build_parameters_tuple

# from hpdta8_params import build_parameters_tuple


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
        self.comment_length: int
        self.width: int
        self.height: int
        self.x_offset: int
        self.y_offset: int
        self.file_type: FileType
        self.data: np.ndarray
        self.comment_string: str
        self.parameters: ParaList
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
            self.data = self.parse_data(file_content[nnn:])
            self.comment_string = file_content[64:nnn].decode("utf-8")
            self.parameters = self.parse_comment(self.comment_string)
            # build_parameters_tuple(self.parameters)

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
                for num in line:
                    file.write(str(num) + "\t")
                file.write("\n")
        return data

    def parse_comment(self, comment: str) -> ParaList:
        """Parse the comment string and return it as a dictionary

        The argument hast to be a 

        args:
            comment: the comment string

        return:
            The returned object is a dictionary of dictionaries. The first level is a dictionary of the comment categories. 
            The second level dictionaries contain the key-value pairs of each category. 

        """
        # build 1st level dictionary
        comment_dict: OrderedDict = OrderedDict()
        # split comment string into category substrings
        comment_list: list = comment.split(sep="\r\n")

        # last entry needs special treatment due to missing line break
        if comment_list[-1].find("[Comment]") > 0:
            corrected_list = re.split(r"(\[Comment\],.*)", comment_list[-1])
            comment_list[-1] = corrected_list[0]
            comment_list.append(corrected_list[1])

        # build 2nd level dictionaries
        for category in comment_list:
            # category name is written in brackets and is extracted first
            catergory_match = re.match(r"\[(.*?)\]\,(.*)", category)
            if catergory_match:
                category_name, category_body = catergory_match.groups()
            else:
                raise ValueError("Category name and/or body could not be parsed.")
            
            key_rex = r"[a-zA-Z0-9\. ]*"
            value_rex = r"[a-zA-Z0-9 ]*"
            quoted_val_rex = r'".*?"'
            comma_or_eos_rex = r"?:,|$"
            key_val_pair_rex = (
                rf"({key_rex})=({value_rex}|{quoted_val_rex})({comma_or_eos_rex})"
            )

            category_dict_with_spaces = OrderedDict(
                re.findall(key_val_pair_rex, category_body)
            )
            category_dict = {
                k.replace(" ", "").replace(".", ""): v
                for k, v in category_dict_with_spaces.items()
            }

            comment_dict[category_name.replace(" ", "")] = category_dict

        if self.verbose:
            print("Comment parsed. This is the resulting dict:")
            with open("params.txt", "w") as params:
                for category in comment_dict:
                    # ToDo: remove
                    # params.write(category + "=namedtuple('" + category + "','")
                    print("-" * 60 + "\n")
                    print(category + ":")
                    print("-" * 60)
                    keys: str = ""
                    for key in comment_dict[category]:
                        value = comment_dict[category][key]
                        print("|\t{:.<22s}:{: <28s}".format(key, value) + "|")
                        keys = keys + key + " "
                    # ToDo: remove
                    # params.write(keys[:-1] + "')\n")
                print("-" * 60 + "\n")
        param_list = build_parameters_tuple(comment_dict)
        return param_list

    def is_compatible(self, other: "StreakImage"):
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
        # ToDo: Implement or purge
        pass

    def get_date(self) -> datetime:
        date_re = re.match(
            r"\"(?P<month>[0-9]{2})\-(?P<day>[0-9]{2})\-(?P<year>[0-9]{4})\"",
            self.parameters.Application.Date,
        )
        time_re = re.match(
            r'"(?P<hour>[0-9]{2})\:(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"',
            self.parameters.Application.Time,
        )
        if date_re and time_re:
            date = date_re.groupdict()
            time = time_re.groupdict()
        else:
            raise ValueError("Date and/or time could not be parsed.")

        datetime_ = datetime(
            int(date["year"]),
            int(date["month"]),
            int(date["day"]),
            int(time["hour"]),
            int(time["minute"]),
            int(time["second"]),
        )

        return datetime_

    def get_json(self) -> str:
        streak_dict: dict = {
            "date": self.get_date(),
            "width": self.width,
            "height": self.height,
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
            "file_type": self.file_type,
            "parameters": self.parameters,
            "data": self.data,
        }
        json_dump = jt_dumps(streak_dict, indent=4)
        return json_dump


# class NumpyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return json.JSONEncoder.default(self, obj)
