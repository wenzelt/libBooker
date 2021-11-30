import sys
import time
from datetime import datetime, timedelta
from enum import auto
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from xvfbwrapper import Xvfb

import config
from models.exceptions import UnknownException
from models.page_enums import PageStatus, SlotStatus
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


def del_booking():
    requests.post(
        url="https://reservierung.ub.uni-muenchen.de/del_entry.php",
        params={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        },
    )


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


def book_slot(slot: SlotStatus, driver: WebDriver, area=config.AREA, room=config.ROOM) -> Tuple[SlotStatus, bool]:
    now = datetime.now()
    next_bookable_date = now + timedelta(days=2)
    room_url = f"https://reservierung.ub.uni-muenchen.de/edit_entry.php?view=day&year={next_bookable_date.year}&month={next_bookable_date.month}&day={next_bookable_date.day}&area={area}&room={room}&period={slot}"
    driver.get(room_url)
    time.sleep(2)
    save_screenshot(driver)
    save_page_source(driver)

    # if not check_bookable(driver.page_source):
    #     return slot, False
    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys(RESERVATION_NAME)
    name_field.submit()

    save_screenshot(driver)
    save_page_source(driver)
    time.sleep(1)
    return slot, True


def start_virtual_displays():
    vdisplay = Xvfb()
    vdisplay.start()
    return vdisplay


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
        slots = [
            book_slot(SlotStatus.EARLY, driver),
            book_slot(SlotStatus.NOON, driver),
            book_slot(SlotStatus.LATE, driver),
            book_slot(SlotStatus.EARLY, driver),
            book_slot(SlotStatus.NOON, driver),
            book_slot(SlotStatus.LATE, driver),
        ]
        print(f"Slots Booked: {slots}")
        print("Done! Closing browser...")
        driver.quit()
    except UnknownException:
        driver.quit()
    if sys.platform == "linux" or sys.platform == "linux2" and v_display:
        v_display.stop()
