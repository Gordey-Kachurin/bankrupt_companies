from settings import URLS, FIERFOX_PROFILE_PATH, PATTERNS, DOWNLOADS_FOLDER
from utils.webdriver_setup import get_driver
from utils.parsers import (
    get_bankrupt_years_and_links,
    download_bankrupcy_file_from_table,
)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
import os

if __name__ == "__main__":
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.mkdir(DOWNLOADS_FOLDER)

    driver = get_driver(FIERFOX_PROFILE_PATH)

    for region in URLS:

        # region_folder_path = os.path.join(DOWNLOADS_FOLDER, region)
        # if not os.path.exists(region_folder_path):
        #     os.mkdir(region_folder_path)

        # TODO: Download files to folders depending on region.
        # Somehow the following is not helping
        # driver.firefox_profile.set_preference("browser.download.dir", region_folder_path)
        # driver.profile.set_preference("browser.download.dir", region_folder_path)

        driver.get(URLS[region] + "/ru")
        bankrupt_years_and_links = get_bankrupt_years_and_links(driver)
        for year, link in bankrupt_years_and_links:
            driver.get(link)
            search_text = PATTERNS["informational_messages"]
            informational_message = driver.find_element(
                By.XPATH, f"//*[ text() = '{search_text}' ]"
            )

            driver.get(informational_message.get_attribute("href"))
            try:
                download_bankrupcy_file_from_table(driver, region, year)
            except NoSuchElementException:
                continue
            # print(os.listdir(DOWNLOADS_FOLDER))

    driver.quit()
