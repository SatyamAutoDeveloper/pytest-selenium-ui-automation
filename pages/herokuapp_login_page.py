import time
from self_healing_agent.heal_wrapper import SmartDriver
from locators.herokuapp_login_locators import *
import logging

logger = logging.getLogger(__name__)


def login_to_herokuapp(driver, username_str, password_str):
    """
    Logs into the Herokuapp login page using the provided credentials.
    Utilizes SmartDriver for AI-assisted element finding.
    """
    smart_driver = SmartDriver(driver)

    logger.info("Attempting to log in to Herokuapp.")

    username_field = smart_driver.find_element_smart(username, description="Username input field")
    password_field = smart_driver.find_element_smart(password, description="Password input field")
    login_btn = smart_driver.find_element_smart(login_button, description="Login button")

    username_field.clear()
    username_field.send_keys(username_str)
    logger.info(f"Entered username: {username_str}")

    password_field.clear()
    password_field.send_keys(password_str)
    logger.info("Entered password.")

    login_btn.click()
    logger.info("Clicked on login button.")
    time.sleep(2)  # Wait for login to process
    logger.info("Login process completed.")

    login_msg_element = smart_driver.find_element_smart(login_msg, description="Login message")
    logger.info(f"Login message displayed: {login_msg_element.text.splitlines()[0].replace('×', '').strip()}")
    return login_msg_element.text.splitlines()[0].replace('×', '').strip()