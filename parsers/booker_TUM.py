import time

from selenium.webdriver.common.by import By

from models.locations import locations_TUM
from parsers.booker_base import Booker


class TUMBooker(Booker):
    def __init__(self, name: str, e_mail: str, identifier: str, arguments: dict):
        super().__init__(arguments)
        self._name = name
        self._e_mail = e_mail
        self._identifier = identifier

    async def book_room(self, area: str = "Stammgelände"):
        location = locations_TUM.get(area)
        self._driver.get(f"https://www.ub.tum.de/reserve/{location}")
        element_mail = self._driver.find_element(By.ID, "edit-anon-mail")

        element_mail.send_keys(self._e_mail)

        element_identifier = self._driver.find_element(By.ID, "edit-field-tum-kennung-und-0-value")

        element_identifier.send_keys(self._identifier)

        element_name = self._driver.find_element(By.ID, "edit-field-tn-name-und-0-value")

        element_name.send_keys(self._name)

        element_radio = self._driver.find_element_by_xpath(
            '//*[@id="edit-field-stud-ma-und"]/div[1]/label'
        )
        element_radio.click()

        element_agreement = self._driver.find_element(
            By.XPATH, '//*[@id="edit-field-benutzungsrichtlinien"]/div/label/span'
        )
        element_agreement.click()

        element_privacy = self._driver.find_element(
            By.XPATH, '//*[@id="edit-field-datenschutzerklaerung"]/div/label/span'
        )
        element_privacy.click()
        time.sleep(2)
        element_privacy.submit()