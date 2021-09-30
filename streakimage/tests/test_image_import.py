import streakimage
import unittest


class TestImageImport(unittest.TestCase):
    def test_C4742_95_import(self):
        with self.assertRaises(None):
            im = streakimage.StreakImage()


if __name__ == "__main__":
    unittest.main()
