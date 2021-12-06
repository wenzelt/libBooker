import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from bookers.booker_base import Booker
from models.exceptions import TooLittleElementsException, ErrorDetectedException
from models.locations import locations_TUM


class TUMBooker(Booker):
    def __init__(self, name: str, e_mail: str, identifier: str, arguments: dict):
        super().__init__(arguments)
        self._name = name
        self._e_mail = e_mail
        self._identifier = identifier
        self._soup = None

    def set_soup(self, html: str):
        self._soup = BeautifulSoup(html, features="html.parser")

    async def book_room(self, area: str = "Stammgelände"):
        location = locations_TUM.get(area)
        self._driver.get(f"https://www.ub.tum.de/reserve/{location}")
        (
            element_agreement,
            element_identifier,
            element_mail,
            element_name,
            element_privacy,
            element_radio,
            len_elements,
        ) = await self.get_input_elements()

        if len_elements == 6:

            await self.send_inputs(
                element_agreement,
                element_identifier,
                element_mail,
                element_name,
                element_privacy,
                element_radio,
            )
        else:
            print("Too little elements found in page")
            raise TooLittleElementsException

    async def send_inputs(
        self,
        element_agreement,
        element_identifier,
        element_mail,
        element_name,
        element_privacy,
        element_radio,
    ):
        element_mail.send_keys(self._e_mail)
        element_identifier.send_keys(self._identifier)
        element_name.send_keys(self._name)
        element_radio.click()
        element_agreement.click()
        element_privacy.click()
        time.sleep(2)
        element_privacy.submit()
        self._driver.implicitly_wait(1)
        self.set_soup(self._driver.page_source)
        self.check_source_for_errors()

    def check_source_for_errors(self):
        if asd := self._soup.find("div", {"class": "messages error"}):
            raise ErrorDetectedException(
                f"We have encountered an error while booking. {asd.text}"
            )

    async def get_input_elements(self):
        element_mail = self._driver.find_element(By.ID, "edit-anon-mail")
        element_identifier = self._driver.find_element(
            By.ID, "edit-field-tum-kennung-und-0-value"
        )
        element_name = self._driver.find_element(
            By.ID, "edit-field-tn-name-und-0-value"
        )
        element_radio = self._driver.find_element_by_xpath(
            '//*[@id="edit-field-stud-ma-und"]/div[1]/label'
        )
        element_agreement = self._driver.find_element(
            By.XPATH, '//*[@id="edit-field-benutzungsrichtlinien"]/div/label/span'
        )
        element_privacy = self._driver.find_element(
            By.XPATH, '//*[@id="edit-field-datenschutzerklaerung"]/div/label/span'
        )
        return (
            element_agreement,
            element_identifier,
            element_mail,
            element_name,
            element_privacy,
            element_radio,
            len(
                [
                    element_agreement,
                    element_identifier,
                    element_mail,
                    element_name,
                    element_privacy,
                    element_radio,
                ]
            ),
        )
