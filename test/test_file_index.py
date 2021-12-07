import unittest

from utilities.file_indexer import FileIndex


class FileIndexTest(unittest.TestCase):
    def test_something(self):
        asd = FileIndex()
        asd.scan()


if __name__ == "__main__":
    unittest.main()
