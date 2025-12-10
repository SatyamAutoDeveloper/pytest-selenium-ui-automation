import logging
import pytest 
from helpers import file_handling
from pages.yatra_hotel_object import *
from pages.yatra_common_object import *

logger = logging.getLogger(__name__)
yatra_hotel_data = file_handling.load_test_data("../testdata/yatra_hotel_data.json")
yatra_common_data = file_handling.load_test_data("../testdata/yatra_common_data.json")

@pytest.mark.positive
def test_search_hotels_in_major_city_for_two_adults(driver):
    logger.info("Starting test: test_search_hotels_in_major_city_for_two_adults")
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."


@pytest.mark.positive
def test_apply_complex_filters_in_hotel_search(driver):
    logger.info("Starting test: test_apply_complex_filters_in_hotel_search")
    expected_filters = [
        yatra_hotel_data["complex_filters"]["star_rating"],
        yatra_hotel_data["complex_filters"]["locality"],
        yatra_hotel_data["complex_filters"]["theme"]
    ]
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."
    apply_complex_filters_on_hotel_search(driver, yatra_hotel_data["complex_filters"]["locality"], yatra_hotel_data["complex_filters"]["theme"])
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."
    assert verify_applied_filters_on_hotel_search(driver, expected_filters) is True, "Applied filters verification failed."


@pytest.mark.negative
def test_selecting_checkout_date_before_checkin_date():
    logger.info("Starting test: test_selecting_checkout_date_before_checkin_date")
    invalid_checkout_days = yatra_hotel_data["invalid_checkout_date"]
    checkout_calendar = yatra_hotel_data["checkout_calendar"]
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    is_disabled = is_checkout_date_disabled_for_invalid_date_selection(invalid_checkout_days, checkout_calendar)
    assert is_disabled == True, "check-out date is not disabled before check-in date."


@pytest.mark.negative
def test_verify_invalid_city_search_shows_empty_list():
    logger.info("Starting test: test_verify_invalid_city_search_shows_empty_list")
    city_name = yatra_hotel_data["invalid_city_name"]
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    is_empty_list_displayed = verify_the_invalid_city_search(city_name)
    assert is_empty_list_displayed is True, "Invalid city search did not show an empty list."


@pytest.mark.edge
def test_search_with_max_rooms(driver):
    logger.info("Starting test: test_search_with_max_rooms")
    rooms_to_add = yatra_hotel_data["add_multiple_guests_rooms"]["rooms_index"]
    guests_per_room = yatra_hotel_data["add_multiple_guests_rooms"]["guests_per_room"]
    expected_room_and_guests_info = yatra_hotel_data["add_multiple_guests_rooms"]["expected_room_and_guests_info"]
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    actual_room_and_guests_info = select_the_search_with_max_room(driver, rooms_to_add, guests_per_room)
    assert actual_room_and_guests_info == expected_room_and_guests_info, "Selected room and guests info does not match."
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."


@pytest.mark.edge
def test_checkout_more_than_15_days_after_checkin():
    logger.info("Starting test: test_checkout_more_than_15_days_after_checkin")
    checkout_days = yatra_hotel_data["checkout_more_than_15_days"]["check_out_after_days"]
    checkout_calendar = yatra_hotel_data["checkout_calendar"] 
    error_msg = yatra_hotel_data["checkout_more_than_15_days"]["expected_error_message"]
    close_yatra_login_popup()
    close_ads_iframe()
    select_yatra_service(yatra_common_data["hotels"])
    is_true = get_more_than_15_days_checkout_error_message(checkout_days, checkout_calendar, error_msg)  # Check-out date: 31 days from today
    logger.info(f"Error message displayed: {is_true}")
    assert is_true is True, "Expected error message not displayed for more than 15 days checkout after check-in." 