from settings import (
    PATTERNS,
    FOLDERS,
    XPATHS_TO_SEARCH_A_ELEMENTS,
    URLS,
    XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES,
)
from selenium.webdriver.common.by import By


import os
import requests
from requests.exceptions import Timeout
from selenium.common.exceptions import NoSuchElementException
from utils.exceptions import DidNotFindInformationalMessage
from utils.file_helpers import rename_and_move


def get_bankrupt_years_and_links(driver):
    """
    EN
    When you use dropdown list as follows
    Legal entities -> Rehabilitation and bankrupcy -> YEAR -> Informational messages
    not all years have "Informational messages" as choise in dropdown.
    But if you go to page of the year you can find link to "Informational messages"

    RU
    При использовании выпадающего списка:
    Юридическим лицам – Реабилитация и банкротство – ГОД* – Информационные сообщения
    не у всех годов есть в списке "Информационные сообщения"W
    Но если перейти на страницу года, можно найти ссылку на "Информационные сообщения"
    """
    # https://www.browserstack.com/guide/find-element-by-text-using-selenium
    text = PATTERNS["legal_entities"]
    ur_lica = driver.find_element(By.XPATH, f"//*[ text() = '{text}' ]")
    ur_lica.click()
    text = PATTERNS["rehabilitation_and_bankrupcy"]
    reabilitaciya_bankrotstvo = driver.find_element(
        By.XPATH, f"//*[ text() = '{text}' ]"
    )
    driver.get(reabilitaciya_bankrotstvo.get_attribute("href"))

    years_list = driver.find_element(
        By.XPATH, "//div[@class='catmenu']/ul[@class='menu']"
    )
    years_list_li_elements = years_list.find_elements(By.TAG_NAME, "li")

    years_and_links = []
    for li in years_list_li_elements:
        a = li.find_element(By.TAG_NAME, "a")
        a_href = a.get_attribute("href")
        if PATTERNS["regex_pattern_for_year"].match(a.text) and PATTERNS[
            "regex_pattern_for_link"
        ].match(a_href):
            print(a.text, a_href)
            years_and_links.append((a.text, a_href))
    return years_and_links


def get_file_and_save_it(link_to_file):
    response = requests.get(link_to_file, allow_redirects=True, timeout=5)
    head_tail = os.path.split(link_to_file)
    if response:  # https://realpython.com/python-requests/
        with open(os.path.join(FOLDERS["temp"], head_tail[1]), "wb") as fp:
            fp.write(response.content)
    else:
        print(f"{response.status_code}: {head_tail[1]}".upper())


def find_links_to_files_and_download(a_elements):

    for a in a_elements:
        if PATTERNS["litigation"].match(a.text):
            if PATTERNS["bankrupcy"] in a.text:
                print(a.text, a.get_attribute("href"))
                try:
                    get_file_and_save_it(a.get_attribute("href"))
                except Timeout:
                    print(f'Не дождался файла по ссылке {a.get_attribute("href")}')
                    continue
                continue
            if PATTERNS["rehabilitation"].match(a.text):
                print(a.text, a.get_attribute("href"))
                try:
                    get_file_and_save_it(a.get_attribute("href"))
                except Timeout:
                    print(f'Не дождался файла по ссылке {a.get_attribute("href")}')
                    continue


def download_files(driver):
    """
    EN
    Downloads Excel files from page.

    RU
    Скачивает файлы Excel со страницы.
    """

    counter = len(XPATHS_TO_SEARCH_A_ELEMENTS)
    for xpath in XPATHS_TO_SEARCH_A_ELEMENTS:
        counter -= 1
        try:
            a_elements = driver.find_elements(By.XPATH, xpath)
            if a_elements != []:
                find_links_to_files_and_download(a_elements)
                break
            else:
                continue
        except NoSuchElementException:
            print(
                f"Ссылки не найдены. Способ поиска: {xpath}. Осталось попыток: {counter}"
            )
            continue
    if counter <= 0:
        raise NoSuchElementException


def get_informational_messages(driver, xpath, key):
    a_elements = driver.find_elements(
        By.XPATH,
        xpath,
    )
    hrefs = []
    for a in a_elements:
        for pattern in PATTERNS["regex_patterns_for_informational_messages"]:
            if pattern.match(a.text):
                hrefs.append(a.get_attribute("href"))

    if hrefs == []:
        information_for_developer = f"Поиск в: {key}"
        print(information_for_developer)
        raise DidNotFindInformationalMessage(information_for_developer)
    return hrefs


def browse_for_files(driver):
    for region in URLS:
        print(region.upper())
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
