import sys
import time
from datetime import datetime, timedelta
from enum import auto
from typing import Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from xvfbwrapper import Xvfb

import config
from models.exceptions import UnknownException
from models.page_enums import PageStatus, SlotStatus
from schedule import lauri_schedule, Schedule
from utilities.folder_manager import save_screenshot, save_page_source

RESERVATION_NAME = config.RESERVATION_NAME

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

LOGIN_URL = "https://reservierung.ub.uni-muenchen.de/admin.php"


def check_login(page_source: str) -> auto:
    if "Bitte anmelden" in page_source:
        return PageStatus.LOGIN
    elif "Anmelden" in page_source:
        return PageStatus.RESERVATION_PAGE
    else:
        return PageStatus.UNDEFINED


def check_bookable(page_source: str) -> bool:
    soup = BeautifulSoup(page_source, features="html.parser")
    policy = soup.find("span", {"id": "policy_check"})
    conflict = soup.find("span", {"id": "conflict_check"})
    if policy:
        if policy.get("class"):
            if "good" not in policy.get("class"):
                print(policy.get("title"))
    if conflict:
        if policy.get("class"):
            if "good" not in conflict.get("class"):
                print(conflict.get("title"))
                return False
            else:
                return True
    return False


def book_slot(
    slot: SlotStatus, driver: WebDriver, area=config.AREA, room=config.ROOM
) -> Tuple[SlotStatus, bool]:
    next_bookable_date = get_next_bookable_date()
    room_url = f"https://reservierung.ub.uni-muenchen.de/edit_entry.php?view=day&year={next_bookable_date.year}&month={next_bookable_date.month}&day={next_bookable_date.day}&area={area}&room={room}&period={slot}"
    driver.get(room_url)
    time.sleep(2)
    save_screenshot(driver)
    save_page_source(driver)

    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys(RESERVATION_NAME)
    name_field.submit()

    save_screenshot(driver)
    save_page_source(driver)
    time.sleep(1)
    return slot, True


def get_next_bookable_date() -> datetime:
    now = datetime.now()
    next_bookable_date = now + timedelta(days=2)
    return next_bookable_date


def start_virtual_displays() -> Xvfb:
    vdisplay = Xvfb()
    vdisplay.start()
    return vdisplay


def book_by_schedule(schedule: Schedule):
    next_date = get_next_bookable_date()
    weekday = next_date.strftime("%A")
    amount_slots = schedule[weekday]
    if amount_slots == 3:
        book_slot(SlotStatus.EARLY, driver),
        book_slot(SlotStatus.NOON, driver),
        book_slot(SlotStatus.LATE, driver),
        book_slot(SlotStatus.EARLY, driver),
        book_slot(SlotStatus.NOON, driver),
        book_slot(SlotStatus.LATE, driver),
    if amount_slots == 2:
        book_slot(SlotStatus.EARLY, driver),
        book_slot(SlotStatus.NOON, driver),
        book_slot(SlotStatus.EARLY, driver),
        book_slot(SlotStatus.NOON, driver),
    if amount_slots == 1:
        book_slot(SlotStatus.EARLY, driver)
        book_slot(SlotStatus.EARLY, driver)


if __name__ == "__main__":
    if sys.platform == "linux" or sys.platform == "linux2":
        v_display = start_virtual_displays()
    driver = webdriver.Chrome()
    try:

        driver.get(LOGIN_URL)
        print("Getting login URL")
        time.sleep(1)

        if check_login(driver.page_source) == PageStatus.LOGIN:
            print("Login page detected. Logging")

            element = driver.find_element(By.ID, "username")
            element.send_keys(USERNAME)
            element = driver.find_element(By.ID, "password")
            element.send_keys(PASSWORD)
            element.submit()

        else:
            print("Maybe already logged in. Skipping...")

        # booking all three slots for
        book_by_schedule(lauri_schedule)
        print("Done! Closing browser...")
        driver.quit()
    except UnknownException:
        driver.quit()
    if sys.platform == "linux" or sys.platform == "linux2" and v_display:
        v_display.stop()
