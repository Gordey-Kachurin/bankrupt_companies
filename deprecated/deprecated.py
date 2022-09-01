from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
    StaleElementReferenceException,
    NoSuchWindowException,
    MoveTargetOutOfBoundsException,
)
import os

from settings import PATTERNS, DOWNLOADS_FOLDER, XPATHS_TO_SEARCH_A_ELEMENTS


def scroll_element_to_center(driver, a):
    # https://www.codegrepper.com/code-examples/python/scroll+to+element+python+selenium
    desired_y = (a.size["height"] / 2) + a.location["y"]
    current_y = (
        driver.execute_script("return window.innerHeight") / 2
    ) + driver.execute_script("return window.pageYOffset")
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def download_file_using_ActionChains(driver, a):
    """
    Much less stable results, than using requests.
    Must be used with close_tabs(driver) function
    'a' ardument is a element (<a> tag).

    """
    try:
        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
            Keys.CONTROL
        ).perform()
    except MoveTargetOutOfBoundsException:
        # driver.execute_script("return arguments[0].scrollIntoView(true);", a)
        scroll_element_to_center(driver, a)
        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
            Keys.CONTROL
        ).perform()


def close_tabs(driver):
    wait_for_download()

    while len(driver.window_handles) > 1:
        try:
            driver.switch_to.window(driver.window_handles[1])
        except IndexError:
            break
        try:
            driver.close()
        except NoSuchWindowException:
            pass
    # Prevents selenium.common.exceptions.NoSuchWindowException after closing tabs
    driver.switch_to.window(driver.window_handles[0])


def wait_for_download():
    # Wait until download is finished
    if os.listdir(DOWNLOADS_FOLDER) != []:
        new_files = os.listdir(DOWNLOADS_FOLDER)
        while ".part" in "".join(new_files):
            print("<<< ", new_files)
            new_files = os.listdir(DOWNLOADS_FOLDER)
