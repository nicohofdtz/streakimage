from datetime import datetime, date
from enum import Enum
import re
import numpy as np
import pandas as pd
import argparse
import json
from json_tricks import dumps as jt_dumps
from collections import OrderedDict, namedtuple
from .hpdta8_params import ParaList, build_parameters_tuple
import struct
import os
from typing import Optional
import configparser


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
            file_path: path to the file to be parsed
            verbose: print verbose comments
            correction: apply camera correction
    """

    def __init__(
        self,
        file_path: str,
        verbose: bool = False,
        correction: bool = False,
        bg=None,
        bg_dict=None,
    ):
        # the hptda fields
        self.comment_length: int
        self.width: int
        self.height: int
        self.x_offset: int
        self.y_offset: int
        self.file_type: FileType
        self.data: pd.DataFrame
        self.comment_string: str
        self.parameters: ParaList
        # the custom fields
        self.verbose: bool = verbose
        self.correction: bool = correction
        self.bg: StreakImage = bg
        self.bg_dict: dict = bg_dict
        self.bg_sub_corr: bool
        self.transient: pd.Series = None

        self.parse_file(file_path)
        if self.verbose:
            print("Comment length:", self.comment_length)
            print("Width:", self.width, "Height:", self.height)
            print("x-offset:", self.x_offset, "y-offset", self.y_offset)
            print("file-type:", self.file_type.name)
            #print("comment:", self.comment_string)
        if self.bg_dict and not self.bg:
            bg_str = f"ST{self.parameters.StreakCamera.TimeRange}_"
            bg_str += f"g{self.parameters.StreakCamera.MCPGain}_"
            bg_str += f"{self.parameters.Acquisition.NrExposure}x"
            bg_str += self.parameters.Acquisition.ExposureTime.replace(" ", "")
            self.bg = self.bg_dict[f"{bg_str}"]
        if self.bg:
            self.apply_bg_subtraction()
        if self.correction:
            self.apply_camera_correction()
        self.shift_0_to_max()

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
            self.bg_sub_corr = self.parameters.Acquisition.BacksubCorr == "1"

    def parse_data(self, binary_data: bytes) -> pd.DataFrame:
        """Parse given data bytes and compile axes

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
        wl_axis, time_axis = self.get_axes(binary_data)
        return pd.DataFrame(data=data, index=time_axis, columns=wl_axis)

    def get_axes(self, binary_data: bytes) -> tuple:
        Axes = namedtuple("Axes", "wl time")
        offset = self.width * 4 + self.height * 4
        wl_axis = np.asarray(
            (struct.unpack_from("f" * (self.width), binary_data[-offset:]))
        )
        time_axis = np.asarray(
            (
                struct.unpack_from(
                    "f" * (self.height), binary_data[(-offset + self.width * 4) :]
                )
            )
        )
        return Axes(wl=wl_axis, time=time_axis)

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
        category_rex = r"(\[[\w ]+?\],(?:.|\n)*?(?=\[|\Z))"
        comment_list = re.split(category_rex, comment)
        comment_list = [item for item in comment_list if item != '']

        # build 2nd level dictionaries
        for category in comment_list:
            #remove linebreaks
            category = category.replace("\r"," - ")
            category = category.replace("\n"," - ")
            # category name is written in brackets and is extracted first
            category_match = re.match(r"\[(.*?)\]\,(.*)", category)
            if category_match:
                category_name, category_body = category_match.groups()
            else:
                raise ValueError(f"Category name and/or body could not be parsed.\ncategory string:\n{category}")

            key_rex = r"[a-zA-Z0-9. ]*"
            value_rex = r"[a-zA-Z0-9\- ]+"
            quoted_val_rex = r'"(?:.|\n)*?"'
            comma_or_eos_rex = r"?:,|$| $|"
            key_val_pair_rex = (
                rf"({key_rex})=({value_rex}|{quoted_val_rex})({comma_or_eos_rex})"
            )

            category_dict_with_spaces = OrderedDict(
                re.findall(key_val_pair_rex, category_body)
            )
            category_dict = {
                k.replace(" ", "").replace(".", ""): v.replace('"', "").strip(" -")
                for k, v in category_dict_with_spaces.items()
            }

            comment_dict[category_name.replace(" ", "")] = category_dict

        if self.verbose:
            print("This is the comment string:")
            print(comment)
            print("Comment parsed. This is the resulting dict:")
            with open("params.txt", "w") as params:
                for category in comment_dict:
                    # ToDo: remove
                    # params.write(category + "=namedtuple('" + category + "','")
                    print("-" * 60 + "\n")
                    print(category + ":")
                    print("-" * 60)
                    if category == "comment":
                        print(comment_dict["Comment"]["UserComment"])
                    else:
                        keys: str = ""
                        for key in comment_dict[category]:
                            value = comment_dict[category][key]
                            print("|\t{:.<22s}:{: <28s}".format(key, value) + "|")
                            keys = keys + key + " "
                print("-" * 60 + "\n")
            print(comment_dict)
        param_list = build_parameters_tuple(comment_dict)
        return param_list

    def is_compatible(self, other: "StreakImage") -> bool:
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

        return True

    def apply_bg_subtraction(self):
        if self.is_compatible(self.bg):
            self.data = self.data - self.bg.data.values
            self.bg_sub_corr = True
        else:
            raise TypeError("Background is not compatible to data.")

    def apply_manual_offset(self, ranges: list):
        offset = 0
        for range_ in ranges:
            a = range_[0][0]
            b = range_[0][1]
            c = range_[1][0]
            d = range_[1][1]

            offset += (self.data.iloc[c:d].loc[:, b:a]).mean().mean()
        self.data -= offset

    def apply_gain_correction(self):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + "/corrections/gain_correction.conf")
        gain = self.parameters.StreakCamera.MCPGain
        cfak = float(config["GAIN-Correction"][gain])
        dat = self.data / cfak
        self.data = dat

    def apply_int_correction(self):
        exp_time = int(self.parameters.Acquisition.ExposureTime.strip(" ms"))
        nr_exp = int(self.parameters.Acquisition.NrExposure)
        cfak = exp_time * nr_exp
        dat = self.data / cfak
        self.data = dat

    def apply_camera_correction(self):
        timerange: str = self.parameters.StreakCamera.TimeRange
        correction = np.load(
            os.path.dirname(__file__)
            + "/corrections/ST"
            + timerange
            + "_correction_"
            + str(self.width)
            + "x"
            + str(self.height)
            + ".npy"
        )
        self.data = self.data / correction

    def shift_0_to_max(self):
        max = self.time_of_max()
        t_max = self.data[max].idxmax()
        self.data.index -= t_max

    def time_of_max(self):
        spec = np.sum(self.data, axis=0)
        return spec.idxmax()

    def shift_time_scale(self, shift_value):
        self.data.index += shift_value

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

    def get_bg_id(self) -> str:
        id = f"bg_{self.parameters.StreakCamera.TimeRange}_"
        id += f"{self.parameters.StreakCamera.MCPGain}_"
        id += f"{self.parameters.Acquisition.NrExposure}x"
        id += f"{self.parameters.Acquisition.ExposureTime.replace(' ','')}"
        return id

        # def get_dimensions(self) -> tuple:
        # return (self.height, self.width)
