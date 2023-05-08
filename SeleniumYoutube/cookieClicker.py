import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service # as a best of practice, use as a Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

driver.get('https://orteil.dashnet.org/cookieclicker/')
driver.implicitly_wait(5)

language = driver.find_element(By.ID, "langSelect-EN")
language.click()
driver.implicitly_wait(10)

cookie = driver.find_element(By.ID, "bigCookie")
cookie_count = driver.find_element(By.ID, "cookies")

items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1, -1, -1)]

# Action Chains
# https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
actions = ActionChains(driver)

for i in range(5000):
    actions.click(cookie)
    actions.perform()    
    count = int(cookie_count.text.split(" ")[0])
    print(count)
    for item in items:
        value = int(item.text)
        if value <= count:
            upgrade_actions = ActionChains(driver)
            upgrade_actions.move_to_element(item)
            upgrade_actions.click()
            upgrade_actions.perform()
