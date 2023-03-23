import threading
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Login not required for Tock. Leave it as false to decrease reservation delay
ENABLE_LOGIN = False
TOCK_USERNAME = "SET_YOUR_USER_NAME_HERE"
TOCK_PASSWORD = "SET_YOUR_PASSWORD_HERE"

# Set your specific reservation month and days
RESERVATION_MONTH = 'April'
#RESERVATION_DAYS = ['30']
RESERVATION_DAYS = ['27','15','8']
RESERVATION_YEAR = '2023'
RESERVATION_TIME_FORMAT = "%I:%M %p"

# Set the time range for acceptable reservation times.
# I.e., any available slots between 5:00 PM and 8:30 PM
EARLIEST_TIME = "12:00 PM"
LATEST_TIME = "9:30 PM"
RESERVATION_TIME_MIN = datetime.strptime(EARLIEST_TIME, RESERVATION_TIME_FORMAT)
RESERVATION_TIME_MAX = datetime.strptime(LATEST_TIME, RESERVATION_TIME_FORMAT)

# Set the party size for the reservation
RESERVATION_SIZE = 2

# Multithreading configurations
NUM_THREADS = 1
THREAD_DELAY_SEC = 5
RESERVATION_FOUND = False

# Time between each page refresh in milliseconds. Decrease this time to
# increase the number of reservation attempts
REFRESH_DELAY_MSEC = 5000

# Chrome extension configurations that are used with Luminati.io proxy.
# Enable proxy to avoid getting IP potentially banned. This should be enabled only if the REFRESH_DELAY_MSEC
# is extremely low (sub hundred) and NUM_THREADS > 1.
ENABLE_PROXY = False
USER_DATA_DIR = '~/Library/Application Support/Google/Chrome'
PROFILE_DIR = 'Default'
# https://chrome.google.com/webstore/detail/luminati/efohiadmkaogdhibjbmeppjpebenaool
EXTENSION_PATH = USER_DATA_DIR + '/' + PROFILE_DIR + '/Extensions/efohiadmkaogdhibjbmeppjpebenaool/1.149.316_0'

# Delay for how long the browser remains open so that the reservation can be finalized. Tock holds the reservation
# for 10 minutes before releasing.
BROWSER_CLOSE_DELAY_SEC = 600

WEBDRIVER_TIMEOUT_DELAY_MS = 3000

MONTH_NUM = {
    'january':   '01',
    'february':  '02',
    'march':     '03',
    'april':     '04',
    'may':       '05',
    'june':      '06',
    'july':      '07',
    'august':    '08',
    'september': '09',
    'october':   '10',
    'november':  '11',
    'december':  '12'
}

class ReserveOnTock():
    def __init__(self):
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        options = self._get_chrome_options()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        print("Driver created:", driver)
        return driver

    def _get_chrome_options(self):
        options = Options()

        if ENABLE_PROXY:
            options.add_argument('--load-extension={}'.format(EXTENSION_PATH))
            options.add_argument('--user-data-dir={}'.format(USER_DATA_DIR))
            options.add_argument('--profile-directory=Default')

        return options

    def teardown(self):
        self.driver.quit()

    def reserve(self):
        global RESERVATION_FOUND
        print("Looking for availability on month: %s, days: %s, between times: %s and %s" % (RESERVATION_MONTH, RESERVATION_DAYS, EARLIEST_TIME, LATEST_TIME))

        if ENABLE_LOGIN:
            self.login_tock()

        while not RESERVATION_FOUND:
            time.sleep(REFRESH_DELAY_MSEC / 1000)
            # For testing purpose: https://www.exploretock.com/84yesler/experience/286812/indoor-dinner-reservation?date=2022-10-29&size=2&time=20%3A00
            #self.driver.get("https://www.exploretock.com/84yesler/experience/286812/search?date=%s-%s-30&size=%s&time=%s" % (RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))

            # LTD Sushi 
            # Website: https://www.exploretock.com/ltdeditionsushi/experience/346803/sushi-bar-reservation
            # Reservations are scheduled for release on October 15, 2022 at 11:00 AM Pacific Daylight Time.
            # Target link: https://www.exploretock.com/ltdeditionsushi/experience/389392/summer-lunch-at-sushi-bar-reservation?date=2022-10-29&size=1&time=19%3A30
            #self.driver.get("https://www.exploretock.com/ivarssalmonhouse/experience/304268/search?date=%s-%s-02&size=%s&time=%s" % (RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))
            self.driver.get("https://www.exploretock.com/ltdeditionsushi/experience/397975//search?date=%s-%s-02&size=%s&time=%s" % (RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))
            
            # Wataru 
            # Website: https://www.exploretock.com/wataru/experience/65237/sushi-bar-reservation
            # Now we reopened sushi bar ”Omakase” on Thursday, Friday, Saturday and Sunday from 7:30 pm.
            # (Sushi bar reservations are accepted up to 1 months in advance. Reservations opens up at 12:00 am on the 1st of each month for the following month.)
            #self.driver.get("https://www.exploretock.com/wataru/experience/65237/search?date=%s-%s-02&size=%s&time=%s" % (RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))

            # Taneda: https://www.exploretock.com/taneda/experience/329211/taneda-omakase
            # Reservation publishes on https://www.instagram.com/tanedaseattle/?hl=en
            # Hours: Wednesday through Sunday 5:15-9:30pm
            #self.driver.get("https://www.exploretock.com/taneda/experience/329211/search?date=%s-%s-02&size=%s&time=%s" % (RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))
            
            WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_DELAY_MS).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.ConsumerCalendar-month")))

            if not self.search_target_day():
                print("No available days found. Continuing next search iteration")
                continue

            WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_DELAY_MS).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "button.Consumer-resultsListItem.is-available")))

            print("Found availability. Sleeping for 10 minutes to complete reservation...")
            RESERVATION_FOUND = True
            time.sleep(BROWSER_CLOSE_DELAY_SEC)

    def login_tock(self):
        self.driver.get("https://www.exploretock.com/ltdeditionsushi/experience/349692/login")
        WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_DELAY_MS).until(expected_conditions.presence_of_element_located((By.NAME, "email")))
        self.driver.find_element(By.NAME, "email").send_keys(TOCK_USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(TOCK_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, ".Button").click()
        WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_DELAY_MS).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".MainHeader-accountName")))

    def search_target_day(self):
        month_object = None

        for month in self.driver.find_elements(By.CSS_SELECTOR, "div.ConsumerCalendar-month"):
            header = month.find_element(By.CSS_SELECTOR, "div.ConsumerCalendar-monthHeading")
            span = header.find_element(By.CSS_SELECTOR, "span.H1")
            print("Encountered month", span.text)

            if RESERVATION_MONTH in span.text:
                month_object = month
                print("Month", RESERVATION_MONTH, "found")
                break

        if month_object is None:
            print("Month", RESERVATION_MONTH, "not found. Ending search")
            return False

        for target_day in RESERVATION_DAYS:
            day_element = self.find_day_element(month_object, target_day)
            if day_element is not None:
                print("Day %s found. Clicking button" % target_day)
                day_element.click()

                if self.search_time():
                    print("Time found")
                    return True

        return False

    def find_day_element(self, month_object, target_day):
        for day in month_object.find_elements(By.CSS_SELECTOR, "button.ConsumerCalendar-day.is-in-month.is-available"):
            span = day.find_element(By.CSS_SELECTOR, "span.B2")
            print("Encountered day: " + span.text)

            if span.text == target_day:
                return day

        return None

    def search_time(self):
        for item in self.driver.find_elements(By.CSS_SELECTOR, "button.Consumer-resultsListItem.is-available"):
            span = item.find_element(By.CSS_SELECTOR, "span.Consumer-resultsListItemTime")
            span2 = span.find_element(By.CSS_SELECTOR, "span")
            print("Encountered time", span2.text)

            available_time = datetime.strptime(span2.text, RESERVATION_TIME_FORMAT)
            if RESERVATION_TIME_MIN <= available_time <= RESERVATION_TIME_MAX:
                print("Time %s found. Clicking button" % span2.text)
                item.click()
                return True

        return False


def month_num(month):
    # TODO error handling
    return MONTH_NUM[month.lower()]


def run_reservation():
    r = ReserveOnTock()
    r.reserve()
    r.teardown()


def execute_reservations():
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=run_reservation)
        threads.append(t)
        t.start()
        time.sleep(THREAD_DELAY_SEC)

    for t in threads:
        t.join()


def continuous_reservations():
    while True:
        execute_reservations()


if __name__ == '__main__':
    continuous_reservations()