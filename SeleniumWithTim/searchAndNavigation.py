# Below shows the old way to use Chrome Web Driver
# As a best of practice, refer to seleniumBasic.py which use web driver as a Service

# Before import, we need to pip install selenium
# Need to download chrome web driver https://chromedriver.chromium.org/downloads
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.techwithtim.net/")

link = driver.find_element(By.LINK_TEXT, "Python Programming")
link.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sow-button-19310003"))
    )
    element.click()

    driver.back()
    driver.back()
    driver.back()
    driver.forward()
    driver.back()
    

# To search a target, use By ID > NAME > CLASS_NAME, ID is most unique
# Selenium returns the first item of the search result, 
# so class is not unique means you might find the one you want

# Find the search box, enter "test" and hit RETURN key
# Need to first impor By before using By.NAME, see: https://selenium-python.readthedocs.io/locating-elements.html
    search = driver.find_element(By.NAME, "s")
    search.clear() # to clear the text already in the text field
    search.send_keys("test")
    search.send_keys(Keys.RETURN)

# Explicit wait https://selenium-python.readthedocs.io/waits.html
# Wait at most 10 sec until expected conditions are met, which is ID called "main" can be located.

    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main")))
    
    articles = main.find_elements(By.TAG_NAME, "article")
    for article in articles:
        header = article.find_element(By.CLASS_NAME, "entry-summary")
        print(header.text)
    time.sleep(5)

finally:
    driver.quit()