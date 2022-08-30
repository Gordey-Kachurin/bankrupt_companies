from settings import PATTERNS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
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
    # Rename and move
    for file in os.listdir(DOWNLOADS_FOLDER):
        # Wait until download is finished
        while ".part" == file[:-5]:
            continue
        new_name = region + " " + year + " "
        renamed = new_name + file
        os.rename(
            os.path.join(DOWNLOADS_FOLDER, file),
            os.path.join(DOWNLOADS_FOLDER, renamed),
        )
        shutil.move(
            os.path.join(DOWNLOADS_FOLDER, renamed), os.path.join(ROOT_FOLDER, region)
        )


def download_bankrupcy_file_from_table(driver, region, year):
    """
    EN
    Downloads Excel file from page.

    RU
    Скачивает файл Excel со страницы.
    """
    try:
        table = driver.find_element(By.TAG_NAME, "table")
        tr_tags = table.find_elements(By.TAG_NAME, "tr")
        for tr in tr_tags:
            try:
                a = tr.find_element(By.TAG_NAME, "a")
                if PATTERNS["litigation"] in a.text:
                    if PATTERNS["bankrupcy"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        a.click()
                        continue
                    if PATTERNS["rehabilitation"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        a.click()

            except NoSuchElementException:
                pass

    except NoSuchElementException:
        try:
            a_elements = driver.find_elements(
                By.XPATH, f"//div[@class='content']//div[@class='field-items']//p/a"
            )
            for a in a_elements:
                if PATTERNS["litigation"] in a.text:
                    if PATTERNS["bankrupcy"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        a.click()
                        continue
                    if PATTERNS["rehabilitation"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        a.click()
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

    # TODO: Опечатки в искомом тексте: 'Информационные сообщение'
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
