import datetime
from datetime import datetime
from enum import Enum


class FileType(Enum):
    """Enum for the file types used by HPD-TA

    can be 8-bit, 16-bit or compressed
    """

    BIT8 = 0
    COMPRESSED = 1  # not used by HPD-TA
    BIT16 = 2


class StreakImage:
    """Parses and holds the data of an recorded image"""

    def __init__(self, file_path):
        self.date: datetime = None
        self.comment_length: int = None
        self.width: int = None
        self.height: int = None
        self.x_offset: int = None
        self.y_offset: int = None
        self.file_type: FileType = None

        self.parse_file(file_path)

    def parse_file(self, file_path):
        file = open(file_path, "rb")
