from helpers.page_helpers import *
from helpers.webdriver_actions import *
from locators.yatra_locators import *
import logging

logger = logging.getLogger(__name__)

def select_yatra_service(service_name):
    """Selects the specified Yatra service tab."""
    click(yatra_services, service_name)

def close_yatra_login_popup():
    """Closes any initial login popup on the Yatra page if present."""
    try:
        logger.info("Closing the Yatra Login Popup")
        click(yatra_popup_close_button)
    except Exception:
        pass  # Popup not present; nothing to close
    
def select_flight_way(way_type):
    """Selects the flight way type (e.g., one-way, round-trip)."""
    logger.info(f"Selecting the flight way: {way_type}")
    click(flight_way_radio_btn, way_type)

def select_tomorrow_date():
    """Selects tomorrow's date."""
    click(date_calendar)
    tomorrow_date = get_tomorrow_date()
    logger.info(f"Selecting the date: {tomorrow_date}")
    click(departure_date_input, tomorrow_date)

def select_city(city_name, default_city):
    """Selects the departure and arrival city."""
    click(open_flight_input, default_city)
    wait_for_element_to_be_visible(flight_input)
    type_value(flight_input, city_name)
    explicit_wait(select_city_option, timeout=2, replace_value=city_name)  # Wait for options to load
    click(select_city_option, city_name)

def departure_city_input(city_name, default_city):
    """Enters the departure city."""
    logger.info(f"Entering the departure city: {city_name}")
    select_city(city_name, default_city)

def arrival_city_input(city_name, default_city):
    """Enters the arrival city."""
    logger.info(f"Entering the arrival city: {city_name}")
    select_city(city_name, default_city)

def select_departure_date():
    """Selects the departure date."""
    logger.info("Selecting the departure date.")
    select_tomorrow_date()

def select_return_date():
    """Selects the return date."""
    logger.info("Selecting the return date.")
    select_tomorrow_date()

def select_traveller_class():
    """Selects traveller and class options."""
    logger.info("Selecting the traveller class.")
    click(traveller_class_input) # Further implementation can be added as needed.

def click_search_button():
    """Clicks the search button."""
    logger.info("Clicking the search button.")
    click(search_flights_button)

def is_search_results_displayed():
    """Checks if search results are displayed."""
    prices_on_different_dates = get_elements_text(prices_on_different_days)
    departure_details = get_elements_text(depart_details_section)
    arrival_details = get_elements_text(arrival_details_section)
    logger.info(f"Prices on different days: {[price.replace('\n', ' ') for price in prices_on_different_dates]}, \
            Departure details: {[departure.replace('\n', ' ') for departure in departure_details]}, \
            Arrival details: {[arrival.replace('\n', ' ') for arrival in arrival_details]}"
           )
    return all([
        is_element_displayed(sorting_options),
        is_element_displayed(prices_on_different_days),
        is_element_displayed(depart_details_section),
        is_element_displayed(arrival_details_section)
    ])

def remove_webklipper_iframe(driver):
    """
    Removes the WebKlipper notification/ad iframe from the page using its fixed ID.
    """
    implicit_wait(5)
    # Use the specific, unique ID of the iframe
    IFRAME_ID = "webklipper-publisher-widget-container-notification-frame"
    
    # JavaScript to find the element by ID and remove it
    script = f"""
    var element = document.getElementById('{IFRAME_ID}');
    if (element) {{
        element.remove();
        console.log('Successfully removed WebKlipper iframe.');
        return true;
    }} else {{
        return false;
    }}
    """
    try:
        driver.execute_script(script)
    except Exception as e:
        print(f"Error executing ad removal script: {e}")
