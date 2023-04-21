import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service # as a best of practice, use as a Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Use detach options to leave brower open even when everything is completed
options = Options()
options.add_experimental_option("detach", True)

#E:\repos\chromedriver.exe
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 

# driver.get('https://www.google.com/')
driver.get('https://www.neuralnine.com/')
driver.maximize_window()

# Find all links on page 
links = driver.find_elements("xpath", "//a[@href]")
for link in links: 
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break

# 	1. Find all div class contains book, which is elementor-column-wrap
# 	2. Find all div box with h2 title PYTHON BIBLE 7 IN 1
#   3. Find the one with only 2 links in it (as this book's div box might be included in a div box with larger scope, like the entire page)
#   3. Find the link and click
# [] means conditions 
# [.//h2[text()[contains(., '7 IN 1')]]] means the text itself contains text "7 IN 1"
# Because there will be multiple containers contain "7 IN 1", we need to find the container with only 2 links in it using [count(.//a)=2]
# //a is getting all the anchor text
book_links = driver.find_elements("xpath", "//div[contains(@class, 'elementor-column-wrap')][.//h2[text()[contains(., '7 IN 1')]]][count(.//a)=2]//a")

# for book_link in book_links:
#     # print(book_link.get_attribute("innerHTML")) 
#     print(book_link)
#     print(book_link.get_attribute("href")) # to get the actual link

book_link = book_links[0].get_attribute("href")
print("Book Link:" + book_link)
# book_links[0].click()

time.sleep(5)

# Open a new tab
driver.execute_script("window.open('');")

# Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])

# Navigate to the new URL in the new tab
driver.get(book_link)

paperbackButtons = driver.find_elements("xpath", "//a[.//span[text()[contains(., 'Paperback')]]]//span[text()[contains(., '$')]]")

for paperbackButton in paperbackButtons:
    print("paperbackButton: " + paperbackButton.get_attribute("innerHTML"))

paperbackButton.click()

buyButtons = driver.find_elements("xpath", "//span[contains(@id, 'submit.buy-now')]")
for buyButton in buyButtons:
    print("buyButton: " + buyButton.get_attribute("innerHTML"))
buyButtons[0].click()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("Script interrupted by the user")