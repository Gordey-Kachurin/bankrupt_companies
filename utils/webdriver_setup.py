from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from settings import FOLDERS
from selenium.webdriver.firefox.options import Options


def set_profile(path_to_profile):
    """
    EN
    Profile folder location: Help -> Troubleshooting Information -> Profile folder

    RU
    Папка с профилем в: Справка -> Информация для рещения проблем -> Папка профиля
    """
    profile = webdriver.FirefoxProfile(path_to_profile)
    # https://stackoverflow.com/questions/18521636/selenium-doesnt-set-downloaddir-in-firefoxprofile
    # https://stackoverflow.com/questions/50321278/how-to-load-firefox-profile-with-python-selenium
    # https://www.selenium.dev/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.firefox_profile.html
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", FOLDERS["temp"])

    return profile


def set_options():
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", FOLDERS["temp"])
    return options


def get_driver(path_to_profile=None):
    """
    EN
    'The main idea is to simplify management of binary drivers for different browsers.'
    1) Create "Personal access token" on GitHub:
    Settings -> Developer settings -> Personal access tokens.
    2) Create .env file in the same folder as main.py
    3) Write to .env: GH_TOKEN=your token

    RU
    Основная идея - упростить работу с драйверами для разных браузеров.
    1) Cоздать "Personal access token" на GitHub:
    Settings -> Developer settings -> Personal access tokens.
    2) Создать файл .env в папке, где размещен main.py
    3) Сделать запись в .env: GH_TOKEN=ваш токен

    """

    options = set_options()
    profile = set_profile(path_to_profile)
    driver = webdriver.Firefox(
        executable_path=GeckoDriverManager().install(),
        firefox_profile=profile,
        options=options,
    )
    driver.maximize_window()
    return driver
