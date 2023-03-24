import time

# LTD Sushi 
# Website: https://www.exploretock.com/ltdeditionsushi/experience/346803/sushi-bar-reservation
# Reservations are scheduled for release on October 15, 2022 at 11:00 AM Pacific Daylight Time.
LTD_URL = "https://www.exploretock.com/ltdeditionsushi/experience/397975"

# Wataru 
# Website: https://www.exploretock.com/wataru/experience/65237/sushi-bar-reservation
# Now we reopened sushi bar ”Omakase” on Thursday, Friday, Saturday and Sunday from 7:30 pm.
# (Sushi bar reservations are accepted up to 1 months in advance. Reservations opens up at 12:00 am on the 1st of each month for the following month.)
WATARU_URL = "https://www.exploretock.com/wataru/experience/65237"

# Taneda: https://www.exploretock.com/taneda/experience/329211/taneda-omakase
# Reservation publishes on https://www.instagram.com/tanedaseattle/?hl=en
# Hours: Wednesday through Sunday 5:15-9:30pm
TANEDA_URL = "https://www.exploretock.com/taneda/experience/329211"

TEST_URL= "https://www.exploretock.com/84yesler/experience/286812"

# Login not required for Tock. Leave it as false to decrease reservation delay
ENABLE_LOGIN = False
TOCK_USERNAME = "SET_YOUR_USER_NAME_HERE"
TOCK_PASSWORD = "SET_YOUR_PASSWORD_HERE"

# Set your specific reservation month and days
RESERVATION_MONTH = 'April'
RESERVATION_DAYS = ['27','15','8']
RESERVATION_YEAR = '2023'
RESERVATION_TIME_FORMAT = "%I:%M %p"

# Set the time range for acceptable reservation times.
# I.e., any available slots between 5:00 PM and 8:30 PM
EARLIEST_TIME = "12:00 PM"
LATEST_TIME = "9:30 PM"

# Set the party size for the reservation
RESERVATION_SIZE = 2

# Multithreading configurations
NUM_THREADS = 5
THREAD_DELAY_SEC = 5
RESERVATION_FOUND = False

# Time between each page refresh in milliseconds. Decrease this time to increase the number of reservation attempts
REFRESH_DELAY_MSEC = 500

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