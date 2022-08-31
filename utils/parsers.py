from settings import PATTERNS, DOWNLOADS_FOLDER
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
    StaleElementReferenceException,
    NoSuchWindowException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os, shutil

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
    # for file in os.listdir(DOWNLOADS_FOLDER):
    #     while ".part" == file[-5:]:
    #         print(file[-5:])
    #         continue
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


def close_tabs(driver):
    # Wait until download is finished
    for file in os.listdir(DOWNLOADS_FOLDER):
        while ".part" == file[-5:]:
            print(file[-5:])
            continue
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        try:
            driver.close()
        except NoSuchWindowException:
            pass
    # Prevents selenium.common.exceptions.NoSuchWindowException after closing tabs
    driver.switch_to.window(driver.window_handles[0])


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
    try:
        table = driver.find_element(By.TAG_NAME, "table")
        tr_tags = table.find_elements(By.TAG_NAME, "tr")
        for tr in tr_tags:
            try:
                a = tr.find_element(By.TAG_NAME, "a")
                if PATTERNS["litigation"].match(a.text):
                    if PATTERNS["bankrupcy"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
                            Keys.CONTROL
                        ).perform()
                        continue
                    if PATTERNS["rehabilitation"].match(a.text):
                        print(a.text, a.get_attribute("href"))
                        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
                            Keys.CONTROL
                        ).perform()
            except NoSuchElementException:
                pass
        close_tabs(driver)

    except NoSuchElementException:
        try:
            a_elements = driver.find_elements(
                By.XPATH, f"//div[@class='content']//div[@class='field-items']//p/a"
            )
            for a in a_elements:
                if PATTERNS["litigation"].match(a.text):
                    if PATTERNS["bankrupcy"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
                            Keys.CONTROL
                        ).perform()
                        continue
                    if PATTERNS["rehabilitation"].match(a.text):
                        print(a.text, a.get_attribute("href"))
                        ActionChains(driver).key_down(Keys.CONTROL).click(a).key_up(
                            Keys.CONTROL
                        ).perform()
            close_tabs(driver)
        except NoSuchElementException:
            raise NoSuchElementException


def get_informational_message(
    driver, regex_search_patterns: list, xpath, root_tag_name
):
    a_elements = driver.find_elements(
        By.XPATH,
        xpath,
    )
    for a in a_elements:
        for pattern in regex_search_patterns:
            if pattern.match(a.text):
                driver.get(a.get_attribute("href"))
                return
    information_for_developer = f"{root_tag_name}: искомого значения нет"
    print(information_for_developer)
    raise DidNotFindInformationalMessage(information_for_developer)


def click_informational_message(driver, regex_search_patterns: list):

    # TODO: Atyrau has multiple Informational messages links in 2021
    try:
        get_informational_message(
            driver,
            regex_search_patterns,
            f"//div[@class='content']/div[contains(@class,'view-taxonomy-term')]/div[@class='view-header']/div[@class='catmenu']/ul[@class='menu']/li/a",
            "view-header",
        )
    except NoSuchElementException:
        try:
            get_informational_message(
                driver,
                regex_search_patterns,
                f"//div[@class='content']/div[contains(@class,'view-taxonomy-term')]/div[@class='view-content']//h3/a",
                "view-content",
            )
        except NoSuchElementException:
            raise NoSuchElementException
    except DidNotFindInformationalMessage:
        try:
            get_informational_message(
                driver,
                regex_search_patterns,
                f"//div[@class='content']/div[contains(@class,'view-taxonomy-term')]/div[@class='view-content']//h3/a",
                "view-content",
            )
        except NoSuchElementException:
            raise NoSuchElementException
        except DidNotFindInformationalMessage:
            raise DidNotFindInformationalMessage(
                "view-header, view-content: нет искомого значения"
            )
