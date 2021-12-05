import time
from datetime import datetime, timedelta
from enum import auto
from typing import Tuple

from selenium.webdriver.common.by import By

import config
from models.exceptions import UnknownException
from models.page_enums import PageStatus, SlotStatus
from parsers.booker_base import Booker
from schedule import Schedule, lauri_schedule
from utilities.folder_manager import save_screenshot, save_page_source


class LMUBooker(Booker):
    def __init__(self, name: str, e_mail: str, identifier: str, arguments: dict):
        super().__init__(arguments)
        self._name = name
        self._e_mail = e_mail
        self._identifier = identifier

    @staticmethod
    def check_login(page_source: str) -> auto:
        if "Bitte anmelden" in page_source:
            return PageStatus.LOGIN
        elif "Anmelden" in page_source:
            return PageStatus.RESERVATION_PAGE
        else:
            return PageStatus.UNDEFINED

    def book_slot(
        self, slot: SlotStatus, area=config.AREA, room=config.ROOM
    ) -> Tuple[SlotStatus, bool]:
        now = datetime.now()
        next_bookable_date = now + timedelta(days=2)
        room_url = f"https://reservierung.ub.uni-muenchen.de/edit_entry.php?view=day&year={next_bookable_date.year}&month={next_bookable_date.month}&day={next_bookable_date.day}&area={area}&room={room}&period={slot}"
        self._driver.get(room_url)
        time.sleep(2)
        save_screenshot(self._driver)
        save_page_source(self._driver)

        name_field = self._driver.find_element(By.ID, "name")
        name_field.send_keys(config.RESERVATION_NAME)
        name_field.submit()

        save_screenshot(self._driver)
        save_page_source(self._driver)
        time.sleep(1)
        return slot, True

    @staticmethod
    def get_next_bookable_date() -> datetime:
        now = datetime.now()
        next_bookable_date = now + timedelta(days=2)
        return next_bookable_date

    def book_by_schedule(self, schedule: Schedule):
        next_date = self.get_next_bookable_date()
        weekday = next_date.strftime("%A")
        amount_slots = schedule[weekday]
        if amount_slots == 3:
            self.book_slot(SlotStatus.EARLY, self._driver),
            self.book_slot(SlotStatus.NOON, self._driver),
            self.book_slot(SlotStatus.LATE, self._driver),
            self.book_slot(SlotStatus.EARLY, self._driver),
            self.book_slot(SlotStatus.NOON, self._driver),
            self.book_slot(SlotStatus.LATE, self._driver),
        if amount_slots == 2:
            self.book_slot(SlotStatus.EARLY, self._driver),
            self.book_slot(SlotStatus.NOON, self._driver),
            self.book_slot(SlotStatus.EARLY, self._driver),
            self.book_slot(SlotStatus.NOON, self._driver),
        if amount_slots == 1:
            self.book_slot(SlotStatus.EARLY, self._driver)
            self.book_slot(SlotStatus.EARLY, self._driver)

    async def book_room(self):
        try:

            self._driver.get("https://reservierung.ub.uni-muenchen.de/admin.php")
            print("Getting login URL")
            time.sleep(1)

            if self.check_login(self._driver.page_source) == PageStatus.LOGIN:
                print("Login page detected. Logging")

                element = self._driver.find_element(By.ID, "username")
                element.send_keys(config.USERNAME)
                element = self._driver.find_element(By.ID, "password")
                element.send_keys(config.PASSWORD)
                element.submit()

            else:
                print("Maybe already logged in. Skipping...")

            # booking all three slots for
            self.book_by_schedule(lauri_schedule)

        except UnknownException:
            self._driver.quit()
