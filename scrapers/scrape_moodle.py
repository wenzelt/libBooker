from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from models.course import MoodleCourse, DocInfo
from models.exceptions import NotLoggedinException, DownloadException
from scrapers.scraper_base import Scraper
from utilities.file_indexer import FileIndexer
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
        for course in self.course_links:
            self._driver.get(course.href)
            self.set_soup(self._driver.page_source)
            document_links = self.get_doc_links()
            for document in document_links:
                if indexer.check_if_file_exists(filename=document.title, course_name=course.title,
                                                extension=document.extension):
                    print(f"Skipping file {document.title} in {course.title}...")
                else:
                    self.download_and_save_file(course, document)

    def download_and_save_file(self, course, document):
        print(f"Downloading file:  {course.title} / {document.title}")
        try:
            response = self._driver.request("GET", document.href)
        except Exception:
            raise DownloadException(f"Could not download file {course.title} / {document.title}")
        save_pdf(response.content, course, document)

    def get_doc_links(self) -> Optional[List[DocInfo]]:
        doc_links = [
            DocInfo(title=i.text.replace(" ", "_"), href=i["href"],
                    extension="pdf" if "pdf" in i.img.get("src") else None)
            for i in self.soup.find_all("a", {"class": "aalink"})
            if i["href"].startswith("https://www.moodle.tum.de/mod/resource/")
        ]
        return doc_links
