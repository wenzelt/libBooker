import datetime
import os
from typing import Tuple

from selenium.webdriver.chrome.webdriver import WebDriver


def save_screenshot(driver: WebDriver):
    filename, path = generate_filespath(".png")
    driver.get_screenshot_as_file(os.path.join(path, filename))


def save_page_source(driver: WebDriver):
    filename, path = generate_filespath(".html")

    # Create the file
    with open(os.path.join(path, filename), "w") as f:
        f.write(driver.page_source)
        f.close()


def generate_filespath(extension_string: str) -> Tuple[str, str]:
    # Find out what the year, month, day and time is
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    # Add the time and the .txt extension as the filename
    filename = time + extension_string
    # Construct the path
    path = "logs/{0}/{1}/{2}/".format(year, month, day)
    # Check if the path exists. If it doesn't create the directories
    if not os.path.exists(path):
        os.makedirs(path)
    return filename, path
