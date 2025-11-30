import logging
import pytest 
from helpers import file_handling
from helpers.webdriver_actions import get_current_url
from pages.yatra_object import *

logger = logging.getLogger(__name__)
yatra_data = file_handling.load_test_data("../testdata/yatra_data.json")


@pytest.mark.positive
def test_one_way_search_flights():
    logger.info("Starting test: test_one_way_search_flights")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    departure_city_input(yatra_data["one_way_flight"]["from_city"], yatra_data["default_departure_city"])
    arrival_city_input(yatra_data["one_way_flight"]["to_city"], yatra_data["default_arrival_city"])
    select_departure_date(yatra_data["one_way_flight"]["departure_after_days"], yatra_data["departure_calendar"])
    click_search_button()
    logger.info("Verifying that search results are displayed for one-way flight search.")
    assert is_search_results_displayed_for_one_way() is True, "Search results are not displayed for one-way flight search."


@pytest.mark.positive
def test_round_trip_search_international_flights():
    logger.info("Starting test: test_round_trip_search_international_flights")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["round_trip"])
    departure_city_input(yatra_data["round_trip_flight"]["from_city"], yatra_data["default_departure_city"])
    arrival_city_input(yatra_data["round_trip_flight"]["to_city"], yatra_data["default_arrival_city"])
    select_departure_date(yatra_data["round_trip_flight"]["departure_after_days"], yatra_data["departure_calendar"])
    implicit_wait(2)
    select_return_date(yatra_data["round_trip_flight"]["return_after_days"], yatra_data["return_calendar"])
    click_search_button()
    logger.info("Verifying that search results are displayed for round-trip flight search.")
    assert is_search_results_displayed_for_round_trip() is True, "Search results are not displayed for round-trip flight search."


@pytest.mark.positive
def test_apply_multiple_valid_filters(driver):
    logger.info("Starting test: Apply multiple valid filters (e.g., Airlines, Price Range, and Departure Time).")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    click_search_button()
    logger.info("Applying multiple filters on the search results.")
    apply_multiple_filters_on_search_results(driver, yatra_data["target_price"], yatra_data["airline_name"], yatra_data["msg_no_flights_found"])
    

@pytest.mark.positive
def test_multi_city_flight_search():
    logger.info("Starting test: test_multi_city_flight_search")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["multi_city"])
    select_multi_cities(yatra_data["multi_city_flight"]["multi_cities"], yatra_data["departure_calendar"])
    logger.info("Verifying that search results are displayed for multi-city flight search.")
    assert is_search_results_displayed_for_multi_city() is True, "Search results are not displayed for multi-city flight search."


@pytest.mark.negative
def test_search_flight_with_past_date():
    logger.info("Starting test: test_search_flight_with_past_date")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    assert is_past_date_disabled(yatra_data["past_departure_days"], yatra_data["departure_calendar"]) is True, "Past Date is not disabled"


@pytest.mark.negative
def test_search_flight_same_city():
    logger.info("Starting test: test_search_flight_same_city")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    arrival_city_input(yatra_data["same_arrival_city"], yatra_data["default_arrival_city"])
    click_search_button()
    logger.info("Verifying that appropriate error message is displayed for same city flight search.")
    assert is_same_city_search_error_displayed(yatra_data["same_city_search_error_msg"]) is True, "Error message for same city flight search is not displayed or not matched."


@pytest.mark.negative
def test_search_flight_with_no_available_flights_route():
    logger.info("Starting test: test_search_flight_with_no_available_flights_route")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    departure_city_input(yatra_data["no_flight"]["from_city"], yatra_data["default_departure_city"])
    arrival_city_input(yatra_data["no_flight"]["to_city"], yatra_data["default_arrival_city"])
    click_search_button()
    logger.info("Verifying that appropriate message is displayed when no flights are available.")
    assert is_no_flights_found_message_displayed(yatra_data["no_flight"]["no_flights_found_msg"]) is True, "No flights found message is not displayed or not matched."


@pytest.mark.edge
def test_search_flight_with_max_allowed_adults_and_infants():
    logger.info("Starting test: test_search_flight_with_max_allowed_adults_and_infants")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    select_passenger(yatra_data["one_way_flight"]["passengers"]["travellers_type"][0], yatra_data["one_way_flight"]["passengers"]["max_adults"])
    implicit_wait(5)
    select_passenger(yatra_data["one_way_flight"]["passengers"]["travellers_type"][1], yatra_data["one_way_flight"]["passengers"]["max_infants"])
    implicit_wait(2)
    click_search_button()
    logger.info("Verifying that search results are displayed for edge case flight search.")
    assert is_search_results_displayed_for_one_way() is True, "Search results are not displayed for edge case flight search."
