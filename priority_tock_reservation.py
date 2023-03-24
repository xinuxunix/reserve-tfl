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

from config import *  # Import the configuration variables from config.py

RESERVATION_TIME_MIN = datetime.strptime(EARLIEST_TIME, RESERVATION_TIME_FORMAT)
RESERVATION_TIME_MAX = datetime.strptime(LATEST_TIME, RESERVATION_TIME_FORMAT)

def generate_url(reservation_year, reservation_month_num, reservation_size, time_code):
    base_url = TEST_URL
    #base_url = LTD_URL
    #base_url = WATARU_URL
    #base_url = TANEDA_URL
    return f"{base_url}/search?date={reservation_year}-{reservation_month_num}-02&size={reservation_size}&time={time_code}"

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
        print(f"Looking for availability on month: {RESERVATION_MONTH}, days: {RESERVATION_DAYS}, between times: {EARLIEST_TIME} and {LATEST_TIME}")

        if ENABLE_LOGIN:
            self.login_tock()

        while not RESERVATION_FOUND:
            time.sleep(REFRESH_DELAY_MSEC / 1000)
            self.driver.get(generate_url(RESERVATION_YEAR, month_num(RESERVATION_MONTH), RESERVATION_SIZE, "22%3A00"))

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