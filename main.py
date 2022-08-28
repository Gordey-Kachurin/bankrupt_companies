from settings import  URLS, FIERFOX_PROFILE_PATH, PATTERNS
from utils.webdriver_setup import get_driver
from utils.parsers import get_bankrupt_years_and_links
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException

if __name__ == '__main__':
    driver = get_driver(FIERFOX_PROFILE_PATH)
    driver.get(URLS['nursultan'] + '/ru')
    bankrupt_years_and_links = get_bankrupt_years_and_links(driver)
    for year, link in bankrupt_years_and_links:
        driver.get(link)
        text = PATTERNS['informational_messages']
        informational_message = driver.find_element(By.XPATH, f"//*[ text() = '{text}' ]")  
        print(informational_message.get_attribute("href"))
        driver.get(informational_message.get_attribute("href"))
        
        
        text = PATTERNS['bankrupcy']
        table = driver.find_element(By.TAG_NAME,  "table") 
        p_tags = table.find_elements(By.TAG_NAME,  "p") 
        for p in p_tags:
            try:
                a = p.find_element(By.TAG_NAME,  "a") 
                if text in a.text:
                    print(a.text, a.get_attribute('href'))
            except NoSuchElementException:
                pass
        
         
        
        
    driver.quit()
  
   