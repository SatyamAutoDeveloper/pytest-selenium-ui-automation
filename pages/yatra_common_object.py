from helpers.page_helpers import *
from helpers.webdriver_actions import *
from locators.yatra_common_locators import *
import logging

logger = logging.getLogger(__name__)


def select_yatra_service(service_name):
    """Selects the specified Yatra service tab."""
    wait_for_element_to_be_visible(yatra_services, timeout=30, replace_value=service_name)
    click(yatra_services, service_name)


def close_yatra_login_popup():
    """Closes any initial login popup on the Yatra page if present."""
    try:
        logger.info("Closing the Yatra Login Popup")
        click(yatra_popup_close_button)
    except Exception:
        pass  # Popup not present; nothing to close


def close_ads_iframe():
    """Closes the ads iframe if present."""
    implicit_wait(10)
    try:
        logger.info("Switching to ads iframe to close it.")
        iframe_switch(ads_iframe_img)
        click(ads_iframe_close_btn)
        logger.info("Ads iframe closed successfully.")
    except Exception:
        logger.info("No ads iframe found to close.")