import logging
import pytest 
from helpers import file_handling
from pages.yatra_flight_object import *
from pages.yatra_common_object import *

logger = logging.getLogger(__name__)
yatra_data = file_handling.load_test_data("../testdata/yatra_flight_data.json")
yatra_common_data = file_handling.load_test_data("../testdata/yatra_common_data.json")

@pytest.mark.positive
def test_one_way_search_flights(load_base_url):
    logger.info("Starting test: test_one_way_search_flights")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    departure_city_input(yatra_data["one_way_flight"]["from_city"], yatra_data["default_departure_city"])
    arrival_city_input(yatra_data["one_way_flight"]["to_city"], yatra_data["default_arrival_city"])
    select_departure_date(yatra_data["one_way_flight"]["departure_after_days"], yatra_data["departure_calendar"])
    click_search_button()
    logger.info("Verifying that search results are displayed for one-way flight search.")
    assert is_search_results_displayed_for_one_way() is True, "Search results are not displayed for one-way flight search."


@pytest.mark.positive
def test_round_trip_search_international_flights(load_base_url):
    logger.info("Starting test: test_round_trip_search_international_flights")
    select_yatra_service(yatra_common_data["flights"])
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
def test_apply_multiple_valid_filters(driver, load_base_url):
    logger.info("Starting test: Apply multiple valid filters (e.g., Airlines, Price Range, and Departure Time).")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    click_search_button()
    logger.info("Applying multiple filters on the search results.")
    apply_multiple_filters_on_search_results(driver, yatra_data["target_price"], yatra_data["airline_name"], yatra_data["msg_no_flights_found"])
    

@pytest.mark.positive
def test_multi_city_flight_search(load_base_url):
    logger.info("Starting test: test_multi_city_flight_search")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["multi_city"])
    select_multi_cities(yatra_data["multi_city_flight"]["multi_cities"], yatra_data["departure_calendar"])
    logger.info("Verifying that search results are displayed for multi-city flight search.")
    assert is_search_results_displayed_for_multi_city() is True, "Search results are not displayed for multi-city flight search."


@pytest.mark.negative
def test_search_flight_with_past_date(load_base_url):
    logger.info("Starting test: test_search_flight_with_past_date")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    assert is_past_date_disabled(yatra_data["past_departure_days"], yatra_data["departure_calendar"]) is True, "Past Date is not disabled"


@pytest.mark.negative
def test_search_flight_same_city(load_base_url):
    logger.info("Starting test: test_search_flight_same_city")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    arrival_city_input(yatra_data["same_arrival_city"], yatra_data["default_arrival_city"])
    click_search_button()
    logger.info("Verifying that appropriate error message is displayed for same city flight search.")
    assert is_same_city_search_error_displayed(yatra_data["same_city_search_error_msg"]) is True, "Error message for same city flight search is not displayed or not matched."


@pytest.mark.negative
def test_search_flight_with_no_available_flights_route(load_base_url):
    logger.info("Starting test: test_search_flight_with_no_available_flights_route")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    departure_city_input(yatra_data["no_flight"]["from_city"], yatra_data["default_departure_city"])
    arrival_city_input(yatra_data["no_flight"]["to_city"], yatra_data["default_arrival_city"])
    click_search_button()
    logger.info("Verifying that appropriate message is displayed when no flights are available.")
    assert is_no_flights_found_message_displayed(yatra_data["no_flight"]["no_flights_found_msg"]) is True, "No flights found message is not displayed or not matched."


@pytest.mark.edge
def test_search_flight_with_max_allowed_adults_and_infants(load_base_url):
    logger.info("Starting test: test_search_flight_with_max_allowed_adults_and_infants")
    adult_traveller = yatra_data["one_way_flight"]["passengers"]["travellers_type"][0]
    max_adult = yatra_data["one_way_flight"]["passengers"]["max_adults"]
    infant_traveller = yatra_data["one_way_flight"]["passengers"]["travellers_type"][1]
    max_infant = yatra_data["one_way_flight"]["passengers"]["max_infants"]
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    select_passenger([adult_traveller, max_adult],[infant_traveller, max_infant])
    implicit_wait(5)
    click_search_button()
    logger.info("Verifying that search results are displayed for edge case flight search.")
    assert is_search_results_displayed_for_one_way() is True, "Search results are not displayed for edge case flight search."


@pytest.mark.edge
def test_input_flight_with_invalid_city(load_base_url):
    logger.info("Starting test: test_input_flight_with_invalid_city")
    select_yatra_service(yatra_common_data["flights"])
    select_flight_way(yatra_data["one_way"])
    logger.info("Verifying that appropriate message is displayed for invalid city flight search.")
    assert enter_invalid_city_and_validate_msg(yatra_data["one_way_flight"]["invalid_city"], yatra_data["default_departure_city"]) is True, "Error message for invalid city flight search is not displayed or not matched."
