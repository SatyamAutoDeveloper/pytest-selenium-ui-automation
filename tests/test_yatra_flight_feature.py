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
    select_yatra_service(yatra_data["flights"])
    select_flight_way(yatra_data["one_way"])
    click_search_button()
    logger.info("Applying multiple filters on the search results.")
    apply_multiple_filters_on_search_results(driver, yatra_data["target_price"], yatra_data["airline_name"])
    