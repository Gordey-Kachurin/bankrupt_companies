from settings import PATTERNS
from selenium.webdriver.common.by import By

def get_bankrupt_years_and_links(driver):
    # https://www.browserstack.com/guide/find-element-by-text-using-selenium
    text = PATTERNS['ur_licam']
    ur_lica = driver.find_element(By.XPATH, f"//*[ text() = '{text}' ]") 
    ur_lica.click()
    text = PATTERNS['rehabilitation_and_bankrupcy']
    reabilitaciya_bankrotstvo = driver.find_element(By.XPATH, f"//*[ text() = '{text}' ]")  
    driver.get(reabilitaciya_bankrotstvo.get_attribute("href"))

    years_list = driver.find_element(By.XPATH, "//div[@class='catmenu']/ul[@class='menu']") 
    years_list_li_elements = years_list.find_elements(By.TAG_NAME, "li")
    
    years_and_links = []
    for li in years_list_li_elements:
        a = li.find_element(By.TAG_NAME, "a")
        a_href = a.get_attribute("href")
        if PATTERNS['regex_pattern_for_year'].match(a.text) and PATTERNS['regex_pattern_for_link'].match(a_href):
            print(a.text, a_href)
            years_and_links.append((a.text, a_href))
    return years_and_links  