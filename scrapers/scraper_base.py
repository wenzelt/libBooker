import sys
from abc import abstractmethod, ABC

from bs4 import BeautifulSoup
from seleniumrequests import Chrome

from utilities.v_display import start_virtual_displays


class Scraper(ABC):
    def __init__(self, arguments: dict):
        self._additional_args = arguments
        if sys.platform == "linux" or sys.platform == "linux2":
            self._v_display = start_virtual_displays()
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('prefs', {
        #     "download.default_directory": "",  # Change default directory for downloads
        #     "download.prompt_for_download": False,  # To auto download the file
        #     "download.directory_upgrade": True,
        #     "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
        # })
        self._driver = Chrome()
        self.soup = None

    @abstractmethod
    def scrape(self):
        raise NotImplementedError

    def set_soup(self, html: str):
        self.soup = BeautifulSoup(html, features="html.parser")
