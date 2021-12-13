import unittest

from utilities.file_indexer import FileIndexer


class FileIndexerTest(unittest.TestCase):
    def test_file_scan(self):
        asd = FileIndexer()
        file_index = asd.scan()
        print(file_index)


if __name__ == "__main__":
    unittest.main()
