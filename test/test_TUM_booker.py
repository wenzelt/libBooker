import unittest

import pytest
from bs4 import BeautifulSoup

from bookers.booker_TUM import TUMBooker
from models.exceptions import ErrorDetectedException


class HTMLLoader:
    bookable = str
    non_bookable = str

    def __init__(self):
        self.bookable = str(open("./html_test/bookable.html").read())
        self.non_bookable = str(open("./html_test/non_bookable.html").read())


class TestClass(unittest.TestCase):
    _data = HTMLLoader()

    def test_set_soup(self):
        test_obj = TUMBooker(
            name="Test", e_mail="test", identifier="test", arguments={}
        )
        with open("html_test/fail_TUM.html") as f:
            asd = f.read()
            test_obj.set_soup(asd)
            assert BeautifulSoup(asd, features="html.parser") == test_obj._soup

    def test_check_source_for_errors(self):
        test_obj = TUMBooker(
            name="Test", e_mail="test", identifier="test", arguments={}
        )
        with open("html_test/fail_TUM.html") as f:
            failing_html = f.read()
            with pytest.raises(ErrorDetectedException):
                test_obj.set_soup(failing_html)
                test_obj.check_source_for_errors()
