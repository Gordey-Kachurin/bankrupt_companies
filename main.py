from settings import (
    URLS,
    FIERFOX_PROFILE_PATH,
    FOLDERS,
    XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES,
)
from utils.webdriver_setup import get_driver
from utils.parsers import (
    get_bankrupt_years_and_links,
    download_files,
    rename_and_move,
    get_informational_messages,
)

from selenium.common.exceptions import NoSuchElementException
import os
from utils.exceptions import DidNotFindInformationalMessage

if __name__ == "__main__":
    for folder in FOLDERS:
        if not os.path.exists(FOLDERS[folder]):
            os.mkdir(FOLDERS[folder])

    driver = get_driver(FIERFOX_PROFILE_PATH)

    for region in URLS:
        print(region)
        region_folder_path = os.path.join(FOLDERS["downloads"], region)
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
                for info_messages_href in hrefs:
                    try:
                        driver.get(info_messages_href)
                        download_files(driver)
                        rename_and_move(
                            FOLDERS["downloads"], FOLDERS["temp"], region, year
                        )
                    except NoSuchElementException:
                        print(
                            f"Для {region} не найдена таблица с перечнем документов за {year}"
                        )
                        continue

    driver.quit()
