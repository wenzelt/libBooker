from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from models.course import MoodleCourse, FileInfo
from models.exceptions import NotLoggedinException
from scrapers.scraper_base import Scraper
from utilities.file_indexer import FileIndexer, FileIndex
from utilities.folder_manager import save_pdf


class ScraperMoodle(Scraper):
    def __init__(self, arguments: dict):
        super().__init__(arguments)
        self._e_mail: str = arguments.get("username")
        self._password: str = arguments.get("password")
        self._soup: Optional[BeautifulSoup] = None
        self._additional_args: dict = arguments
        self.course_links: Optional[List[MoodleCourse]] = None

    async def scrape(self):
        self._driver.get("https://www.moodle.tum.de/my/")
        if self._driver.current_url == "https://www.moodle.tum.de/login/index.php":
            print("login_detected")
            await self.login()

    def set_soup(self, html: str):
        self.soup = BeautifulSoup(html, features="html.parser")

    async def send_inputs_and_submit(self, username_field, password_field):
        username_field.send_keys(self._e_mail)
        password_field.send_keys(self._password)
        password_field.send_keys(Keys.ENTER)

    async def login(self):
        element = self._driver.find_element(
            By.XPATH, "//a[contains(text(), 'TUM LOGIN')]"
        )
        element.click()
        self._driver.implicitly_wait(1)
        username_field = self._driver.find_element(By.ID, "username")
        password_field = self._driver.find_element(By.ID, "password")

        await self.send_inputs_and_submit(username_field, password_field)
        await self.check_logged_in()
        self.set_soup(self._driver.page_source)
        await self.set_all_course_links()

        await self.download_all()
        pass

    async def set_all_course_links(self):
        active_courses = self.soup.find("div", {"id": "coc-courselist"})
        self.course_links = [
            MoodleCourse(title=i["title"].replace("/", "_"), href=i["href"])
            for i in active_courses.find_all("a", {"title": True, "href": True})
            if i["href"].startswith("https://www.moodle.tum.de/course/view.php?")
        ]

    async def check_logged_in(self):
        if self._driver.current_url != "https://www.moodle.tum.de/my/":
            raise NotLoggedinException

    async def download_all(self):
        indexer = FileIndexer()
        file_index = indexer.scan()
        for course in self.course_links:
            self._driver.get(course.href)
            self.set_soup(self._driver.page_source)
            document_links = self.get_doc_links()
            x = [i for i in file_index if i.folder == course.title]
            current_course_index = x[0] if x else FileIndex(folder=None, files=[])

            for document in tqdm(document_links):
                self.download_file(
                    course, document
                ) if f"{document.title}.pdf" not in current_course_index.files else print(
                    "File in index. Skipping..."
                )

    def download_file(self, course, document):
        response = self._driver.request("GET", document.href)
        save_pdf(response.content, course, document)

    def get_doc_links(self) -> Optional[List[FileInfo]]:
        doc_links = [
            FileInfo(title=i.text.replace(" ", "_"), href=i["href"])
            for i in self.soup.find_all("a", {"class": "aalink"})
            if i["href"].startswith("https://www.moodle.tum.de/mod/resource/")
        ]
        return doc_links
