import os
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


def set_profile(path_to_profile):
    """
    https://stackoverflow.com/questions/22685755/retaining-cache-in-firefox-and-chrome-browser-selenium-webdriver
    https://stackoverflow.com/questions/50321278/how-to-load-firefox-profile-with-python-selenium
    https://www.selenium.dev/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.firefox_profile.html
    EN
    Profile folder location: Help -> Troubleshooting Information -> Profile folder
    
    RU
    Папка с профилем в: Справка -> Информация для рещения проблем -> Папка профиля
    """
    fp = webdriver.FirefoxProfile(path_to_profile)
    return fp

def get_driver(path_to_profile=None):
    """
    https://github.com/SergeyPirogov/webdriver_manager
    EN 'The main idea is to simplify management of binary drivers for different browsers.'
    RU Основная идея - упростить работу с драйверами для разных браузеров.
    
    EN
    1) Create "Personal access token" on GitHub: Settings -> Developer settings -> Personal access tokens.
    2) Assign token to 'GH_TOKEN' environment variable
    
    RU
    1) Cоздать "Personal access token" на GitHub в разделе
    Settings -> Developer settings -> Personal access tokens.
    Токен присвоить в переменную среду 'GH_TOKEN'
    Переменную среду разместить в файле .env
    
    """
    fp = set_profile(path_to_profile)
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=fp)
    driver.maximize_window()
    return driver