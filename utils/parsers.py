from settings import PATTERNS, DOWNLOADS_FOLDER, XPATHS_TO_SEARCH_A_ELEMENTS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
)

import os, shutil
import requests
from requests.exceptions import Timeout
from .exceptions import DidNotFindInformationalMessage


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


def rename_and_move(ROOT_FOLDER, DOWNLOADS_FOLDER, region, year):
    # # Wait until download is finished
    # wait_for_download() deprecated. Used with
    # Rename and move
    for file in os.listdir(DOWNLOADS_FOLDER):
        new_name = region + " " + year + " "
        renamed = new_name + file
        os.rename(
            os.path.join(DOWNLOADS_FOLDER, file),
            os.path.join(DOWNLOADS_FOLDER, renamed),
        )
        shutil.move(
            os.path.join(DOWNLOADS_FOLDER, renamed), os.path.join(ROOT_FOLDER, region)
        )


def download_file(link_to_file):
    r = requests.get(link_to_file, allow_redirects=True, timeout=5)
    head_tail = os.path.split(link_to_file)
    with open(os.path.join(DOWNLOADS_FOLDER, head_tail[1]), "wb") as fp:
        fp.write(r.content)


def click_rehabilitation_and_bankrupcy_elements(a_elements):

    for a in a_elements:
        if PATTERNS["litigation"].match(a.text):
            if PATTERNS["bankrupcy"] in a.text:
                print(a.text, a.get_attribute("href"))
                try:
                    download_file(a.get_attribute("href"))
                except Timeout:
                    print(f'Не дождался файла по ссылке {a.get_attribute("href")}')
                    continue
                continue
            if PATTERNS["rehabilitation"].match(a.text):
                print(a.text, a.get_attribute("href"))
                try:
                    download_file(a.get_attribute("href"))
                except Timeout:
                    print(f'Не дождался файла по ссылке {a.get_attribute("href")}')
                    continue


def download_bankrupcy_file_from_table(driver):
    """
    EN
    Downloads Excel file from page.
    ActionChains handles both cases when file is there or not found

    RU
    Скачивает файл Excel со страницы.
    ActionChains обрабатывает оба случая, когда файл есть или не найден.
    """
    # TODO: Kostanai unexpected table structure in 2017

    counter = len(XPATHS_TO_SEARCH_A_ELEMENTS)
    for xpath in XPATHS_TO_SEARCH_A_ELEMENTS:
        counter -= 1
        try:
            a_elements = driver.find_elements(By.XPATH, xpath)
            if a_elements != []:
                click_rehabilitation_and_bankrupcy_elements(a_elements)
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
                # driver.get(a.get_attribute("href"))
                # return
    if hrefs == []:
        information_for_developer = f"Поиск в: {key}"
        print(information_for_developer)
        raise DidNotFindInformationalMessage(information_for_developer)
    return hrefs
