from settings import  URLS, FIERFOX_PROFILE_PATH
from utils.webdriver_setup import get_driver
from utils.parsers import get_bankrupt_years_and_links


if __name__ == '__main__':
    driver = get_driver(FIERFOX_PROFILE_PATH)
    driver.get(URLS['nursultan'] + '/ru')
    bankrupt_years_and_links = get_bankrupt_years_and_links(driver)
    
 
    driver.quit()
  
   