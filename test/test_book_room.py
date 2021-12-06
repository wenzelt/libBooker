import unittest

from book_room import check_bookable


class HTMLLoader:
    bookable = str
    non_bookable = str

    def __init__(self):
        self.bookable = str(open("./html_test/bookable.html").read())
        self.non_bookable = str(open("./html_test/non_bookable.html").read())


class TestClass(unittest.TestCase):
    _data = HTMLLoader()

    def test_bookable(self):
        assert check_bookable(self._data.bookable) == True

    def test_non_bookable(self):
        assert check_bookable(self._data.non_bookable) == False
