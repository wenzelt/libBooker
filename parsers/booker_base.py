import sys
from abc import abstractmethod, ABC

from selenium import webdriver

from utilities.v_display import stop_virtual_displays


class Booker(ABC):
    def __init__(self, arguments: dict):
        self._additional_args = arguments
        if sys.platform == "linux" or sys.platform == "linux2":
            self._v_display = stop_virtual_displays()
        self._driver = webdriver.Chrome()

    @abstractmethod
    def book_room(self):
        raise NotImplementedError
