
from configparser import ConfigParser
import logging
import time
from helpers.webdriver_actions import load_url
from pages.herokuapp_login_page import login_to_herokuapp

CONFIG = ConfigParser()
CONFIG.read('config.ini')
DUMMY_BASE_URL = CONFIG.get('DUMMY_BASE_URL', 'Settings', fallback='https://the-internet.herokuapp.com/login')
USERNAME = CONFIG.get('USERNAME', 'Settings', fallback='tomsmith')
PASSWORD = CONFIG.get('PASSWORD', 'Settings', fallback='SuperSecretPassword!')

logger = logging.getLogger(__name__)


def test_login_to_herokuapp(driver):
    logger.info("Starting test: test_login_to_herokuapp")
    logger.info(f"Loading herokuapp login URL: {DUMMY_BASE_URL}")
    load_url(DUMMY_BASE_URL)
    time.sleep(2)  # Wait for page to load
    logger.info(f"Current URL after loading herokuapp login page: {driver.current_url}")
    login_message = login_to_herokuapp(driver, USERNAME, PASSWORD)
    assert login_message == "You logged into a secure area!", "Login message did not match expected text."