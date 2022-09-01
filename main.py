from re import L
from settings import (
    ROOT_FOLDER,
    URLS,
    FIERFOX_PROFILE_PATH,
    PATTERNS,
    DOWNLOADS_FOLDER,
    XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES,
)
from utils.webdriver_setup import get_driver
from utils.parsers import (
    get_bankrupt_years_and_links,
    download_bankrupcy_file_from_table,
    rename_and_move,
    get_informational_messages,
)
import shutil
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
import os
from utils.exceptions import DidNotFindInformationalMessage

if __name__ == "__main__":
    if not os.path.exists(ROOT_FOLDER):
        os.mkdir(ROOT_FOLDER)
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.mkdir(DOWNLOADS_FOLDER)

    driver = get_driver(FIERFOX_PROFILE_PATH)

    for region in URLS:
        print(region)
        region_folder_path = os.path.join(ROOT_FOLDER, region)
        if not os.path.exists(region_folder_path):
            os.mkdir(region_folder_path)

        # TODO: Download files to folders depending on region.
        # Somehow the following is not helping
        # driver.firefox_profile.set_preference("browser.download.dir", region_folder_path)
        # driver.profile.set_preference("browser.download.dir", region_folder_path)

        driver.get(URLS[region] + "/ru")
        bankrupt_years_and_links = get_bankrupt_years_and_links(driver)
        for year, link in bankrupt_years_and_links:
            driver.get(link)

            info_messages_hrefs = []
            for key in XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES.keys():
                try:
                    hrefs = get_informational_messages(
                        driver, XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES[key], key
                    )
                    if hrefs != []:
                        info_messages_hrefs.append(hrefs)

                except DidNotFindInformationalMessage as e:
                    print(
                        f"{region}, {year}: не найдена ссылка на Информационные сообщения. {e.message}."
                    )
                    continue
                except NoSuchElementException:
                    print(f"{region}, {year}: не найдены элементы для поиска.")
                    continue

            print(region, year)
            print(info_messages_hrefs)
            # TODO Одинаковые файлы в разных ссылках на информационные сообщения.
            for hrefs in info_messages_hrefs:
                for href in hrefs:
                    try:
                        driver.get(href)
                        download_bankrupcy_file_from_table(driver)
                        rename_and_move(ROOT_FOLDER, DOWNLOADS_FOLDER, region, year)
                    except NoSuchElementException:
                        print(
                            f"Для {region} не найдена таблица с перечнем документов за {year}"
                        )
                        continue

    driver.quit()
