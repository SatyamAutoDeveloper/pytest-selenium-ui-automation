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


def navigate_to_date_in_calendar(target_date):
    """Navigate the calendar to the target date by clicking the next button until the date is visible."""
    while is_element_not_present(date_input, replace_value=target_date):
        click(calendar_next_button)

def select_date(days_from_today, journey_type):
    """Selects a date based on days from today."""
    click(date_calendar, journey_type)
    logger.info("Opening the calendar.")
    selected_date = get_formatted_date_in_days(days_from_today)
    logger.info(f"Selecting the date: {selected_date}")
    if not is_element_present(date_input, replace_value=selected_date):
        logger.info(f"Date {selected_date} is not visible, navigating to next month in calendar.")
        navigate_to_date_in_calendar(selected_date)
    double_click_on_element(date_input, selected_date)

def select_city(city_name, default_city):
    """Selects the departure and arrival city."""
    click(open_flight_input, default_city)
    wait_for_element_to_be_visible(flight_input)
    type_value(flight_input, city_name)
    explicit_wait(select_city_option, timeout=5, replace_value=city_name)  # Wait for options to load
    click(select_city_option, city_name)

def departure_city_input(city_name, default_city):
    """Enters the departure city."""
    logger.info(f"Entering the departure city: {city_name}")
    select_city(city_name, default_city)

def arrival_city_input(city_name, default_city):
    """Enters the arrival city."""
    logger.info(f"Entering the arrival city: {city_name}")
    select_city(city_name, default_city)

def select_departure_date(days_from_today, journey_type):
    """Selects the departure date."""
    logger.info("Selecting the departure date.")
    select_date(days_from_today, journey_type)

def select_return_date(days_from_today, journey_type):
    """Selects the return date."""
    logger.info("Selecting the return date.")
    select_date(days_from_today, journey_type)

def select_traveller_class():
    """Selects traveller and class options."""
    logger.info("Selecting the traveller class.")
    click(traveller_class_input) # Further implementation can be added as needed.

def click_search_button():
    """Clicks the search button."""
    logger.info("Clicking the search button.")
    click(search_flights_button)

def is_search_results_displayed_for_one_way():
    """Checks if search results are displayed for one way flights."""
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


def is_search_results_displayed_for_round_trip():
    """Checks if search results are displayed for round trip flights."""
    wait_for_element_to_be_visible(round_trip_sorting_by_price, timeout=30)
    price_based_sorting = get_elements_text(round_trip_sorting_by_price)
    round_trip_details = get_elements_text(round_trip_details_section)
    logger.info(f"Prices based on value: {[price.replace('\n', ' ') for price in price_based_sorting]}, \
            Round trip details: {[detail.replace('\n', ' ') for detail in round_trip_details]}, \
            Number of flights: {len(find_elements(no_of_flights))}"
           )
    return all([
        is_element_displayed(round_trip_sorting_by_price),
        is_element_displayed(round_trip_details_section)
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


def set_price_filter(driver, target_price):
    """Sets the price filter using the slider."""
    logger.info("Setting the price filter using the slider.")
    min_price = get_element_attribute(min_price_elem, "data-value")
    max_price = get_element_attribute(max_price_elem, "data-value")

    cost_slider = find_element(price_slider)  # Ensure slider is loaded
    slider_width = cost_slider.size['width']

    logger.info(f"Slider width in pixels: {slider_width}, Min price: {min_price}, Max price: {max_price}")
    set_horizontal_slider(driver, price_slider_handle, slider_width, int(min_price), int(max_price), target_price)
    actual_price = get_element_text(target_price_elem)
    assert 9950 <= int(actual_price.replace(',', '')) <= 10050, \
        f"Price filter not set correctly. Expected: {target_price}, Found: {actual_price.replace(',', '')}"


def select_departure_time_range():
    """Selects the departure time range filter."""
    logger.info("Selecting the departure time range filter.")
    click(depart_time_range)


def select_airlines(airline):
    """Selects the specified airlines in the filter."""
    logger.info(f"Selecting airline filter: {airline}")
    click(select_flight, airline)


def apply_multiple_filters_on_search_results(driver, target_price, airline):
    """Applies multiple filters on the search results."""
    click(more_filters)
    logger.info(f"Setting price filter to: {target_price}")
    set_price_filter(driver, target_price)
    logger.info("Selecting departure time range filter: 6AM - 12PM")
    select_departure_time_range()
    logger.info(f"Selecting airline filter: {airline}")
    select_airlines(airline)
    click(apply_filter_btn)