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
    """Parses and holds the data of an recorded image
    
        args:
            file_path: Path to the file to be parsed

    """

    def __init__(self, file_path: str):
        self.date: datetime
        self.comment_length: int
        self.width: int
        self.height: int
        self.x_offset: int
        self.y_offset: int
        self.file_type: FileType
        self.data: list

        self.parse_file(file_path)
        # print("Date:", self.date)
        print("Comment length:", self.comment_length)
        print("Width:", self.width, "Height:", self.height)
        print("x-offset:", self.x_offset, "y-offset", self.y_offset)
        print("file-type:", self.file_type.name)

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
            self.comment = file_content[64:nnn]
            self.data = self.parse_data(file_content[nnn:])

    def parse_data(self, binary_data: bytes):
        """Parse given data bytes to 2d list

        args:
            binary_data: The part of the file containing the intensity data.

        """
        data = [[0] * self.width for i in range(self.height)]
        byte_per_pixel = 2 if self.file_type == FileType.BIT8 else 4
        from_ = 0
        to = byte_per_pixel

        for y in range(0, self.height):
            for x in range(0, self.width):
                data[x][y] = int.from_bytes(
                    binary_data[from_:to], byteorder="little", signed=False
                )
                from_ += byte_per_pixel
                to += byte_per_pixel
        with open("data.txt", "w") as file:
            for line in data:
                file.writelines(str(line)[1:-1] + "\n")
        return data
