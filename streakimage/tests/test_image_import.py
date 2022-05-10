from os import error, path
import streakimage
import unittest

from streakimage.image import CameraModel



def get_tpath(path_: str) -> str:
    return path.join("./streakimage/tests/", path_)
class TestImageImport(unittest.TestCase):
    def test_C4742_95_import(self):
        try:
            im = streakimage.StreakImage(
                file_path="./streakimage/tests/test_imgs/20200826 101 DN216_MgZnO_200804 00a P1 000mV.img"
            )
        except error:
            self.fail("Import failed")

    def test_C4742_95_12ER_import(self):
        try:
            im = streakimage.StreakImage(
                file_path="./streakimage/tests/test_imgs/190703 01 TRPL Z1 20x10s.img"
            )
        except error:
            self.fail("Import Failed")


class TestEnums(unittest.TestCase):
    def test_camera_enum(self):
        self.assertEqual(CameraModel.C4742_95_12ER.value, "ir")
        self.assertEqual(CameraModel.C4742_95.value, "uvvis")

class TestCorrections(unittest.TestCase):
    def setUp(self):
        self.img = streakimage.StreakImage()

    def test_ir_camera_correction(self):


if __name__ == "__main__":
    unittest.main()
