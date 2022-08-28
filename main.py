from settings import URLS, FIERFOX_PROFILE_PATH, PATTERNS, DOWNLOADS_FOLDER
from utils.webdriver_setup import get_driver
from utils.parsers import get_bankrupt_years_and_links
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
import os

if __name__ == "__main__":
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.mkdir(DOWNLOADS_FOLDER)

    driver = get_driver(FIERFOX_PROFILE_PATH)
    driver.get(URLS["nursultan"] + "/ru")
    bankrupt_years_and_links = get_bankrupt_years_and_links(driver)
    for year, link in bankrupt_years_and_links:
        driver.get(link)
        text = PATTERNS["informational_messages"]
        informational_message = driver.find_element(
            By.XPATH, f"//*[ text() = '{text}' ]"
        )
        print(informational_message.get_attribute("href"))
        driver.get(informational_message.get_attribute("href"))

        try:
            table = driver.find_element(By.TAG_NAME, "table")
            p_tags = table.find_elements(By.TAG_NAME, "p")
            for p in p_tags:
                try:
                    a = p.find_element(By.TAG_NAME, "a")
                    if PATTERNS["bankrupcy"] in a.text:
                        print(a.text, a.get_attribute("href"))
                        a.click()
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            print(
                f"Для {URLS['nursultan']} найдена таблица с перечнем документов за {year}"
            )
            continue

    driver.quit()
