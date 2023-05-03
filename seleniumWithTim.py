# Below shows the old way to use Chrome Web Driver
# As a best of practice, refer to seleniumBasic.py which use web driver as a Service

# Before import, we need to pip install selenium
# Need to download chrome web driver https://chromedriver.chromium.org/downloads
from selenium import webdriver
PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.techwithtim.net/")
print(driver.title)
driver.quit()