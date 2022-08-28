import requests
from bs4 import BeautifulSoup
from settings import PATTERNS, URLS, PATH_TO_FIERFOX_PROFILE
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import os
from utils.webdriver_setup import get_driver
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    driver = get_driver(PATH_TO_FIERFOX_PROFILE)
    driver.get(URLS['nursultan'] + '/ru')
    # https://www.browserstack.com/guide/find-element-by-text-using-selenium
    ur_lica = driver.find_element(By.XPATH, "//*[ text() = 'Юридическим лицам' ]") 
    ur_lica.click()
    reabilitaciya_bankrotstvo = driver.find_element(By.XPATH, "//*[ text() = 'Реабилитация и банкротство' ]")  
     
    print("Value is: %s" % reabilitaciya_bankrotstvo.get_attribute("href"))
    driver.get(reabilitaciya_bankrotstvo.get_attribute("href"))
    # print(ur.tag_name)
 
    driver.quit()
  
   