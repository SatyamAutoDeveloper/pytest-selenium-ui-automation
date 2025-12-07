from helpers.page_helpers import *
from helpers.webdriver_actions import *
from locators.yatra_hotel_locators import *
import logging

logger = logging.getLogger(__name__)


def select_city(driver, city_name):
    """Selects the departure and arrival city."""
    logger.info(f"Selecting the city: {city_name}")
    wait_for_element_to_be_visible(open_hotel_city)
    click(open_hotel_city)
    wait_for_element_to_be_visible(hotel_city_input)
    type_value(hotel_city_input, city_name)
    wait_for_element_to_be_visible(select_hotel_city_list)
    scroll_element_into_view_in_side_bar(driver, select_hotel_city_list, select_hotel_city_list_item)
    click(select_hotel_city_list_item)


def navigate_to_date_in_calendar(target_date, days_from_today):
    """Navigate the calendar to the target date by clicking the next button until the date is visible."""
    while is_element_not_present(select_date_in_calendar, replace_value=target_date):
        if days_from_today < 0:
            click(calendar_prev_btn)
        else:
            click(calendar_next_btn)


def select_date(days_from_today, index):
    """Selects a date based on days from today."""
    click(open_date_calendar, index)
    logger.info("Opening the calendar.")
    selected_date = get_formatted_date_in_days(days_from_today)
    logger.info(f"Selecting the date: {selected_date}")
    if not is_element_present(select_date_in_calendar, replace_value=selected_date):
        logger.info(f"Date {selected_date} is not visible, navigating to the month in calendar.")
        navigate_to_date_in_calendar(selected_date, days_from_today)
    if days_from_today < 0:
        logger.info(f"Checking if past date {selected_date} is disabled.")
        is_disabled = get_element_attribute(select_date_in_calendar, "aria-disabled", replace_value=selected_date)
        logger.info(f"Date {selected_date} disabled status: {is_disabled}")
        if is_disabled == "true":
            logger.info(f"{selected_date} is disabled as this date is already past")
            return True
        else:
            logger.error(f"{selected_date} is not disabled, test failed.")
            return False    
    double_click_on_element(select_date_in_calendar, selected_date)


def click_search_button():
    """Clicks the search button."""
    logger.info("Clicking the search button.")
    click(search_hotels_button)


def verify_hotel_search_results_displayed():
    """Verifies that hotel search results are displayed."""
    logger.info("Verifying that hotel search results are displayed.")
    wait_for_element_to_be_visible(hotel_search_results_section)
    available_hotel_text = get_element_text(hotel_search_results_section)
    logger.info(f"Available Hotel Options: {available_hotel_text}")
    return "hotel options available" in available_hotel_text.lower()