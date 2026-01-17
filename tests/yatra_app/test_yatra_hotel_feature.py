import logging
import pytest 
from helpers import file_handling
from pages.yatra_hotel_object import *
from pages.yatra_common_object import *

logger = logging.getLogger(__name__)
yatra_hotel_data = file_handling.load_test_data("../testdata/yatra_hotel_data.json")
yatra_common_data = file_handling.load_test_data("../testdata/yatra_common_data.json")


@pytest.mark.positive
def test_search_hotels_in_major_city_for_two_adults(driver, load_base_url):
    logger.info("Starting test: test_search_hotels_in_major_city_for_two_adults")
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."


@pytest.mark.positive
def test_apply_complex_filters_in_hotel_search(driver, load_base_url):
    logger.info("Starting test: test_apply_complex_filters_in_hotel_search")
    expected_filters = [
        yatra_hotel_data["complex_filters"]["star_rating"],
        yatra_hotel_data["complex_filters"]["locality"],
        yatra_hotel_data["complex_filters"]["theme"]
    ]
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."
    apply_complex_filters_on_hotel_search(driver, yatra_hotel_data["complex_filters"]["locality"], yatra_hotel_data["complex_filters"]["theme"])
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."
    assert verify_applied_filters_on_hotel_search(driver, expected_filters) is True, "Applied filters verification failed."


@pytest.mark.negative
def test_selecting_checkout_date_before_checkin_date(load_base_url):
    logger.info("Starting test: test_selecting_checkout_date_before_checkin_date")
    invalid_checkout_days = yatra_hotel_data["invalid_checkout_date"]
    checkout_calendar = yatra_hotel_data["checkout_calendar"]
    select_yatra_service(yatra_common_data["hotels"])
    is_disabled = is_checkout_date_disabled_for_invalid_date_selection(invalid_checkout_days, checkout_calendar)
    assert is_disabled == True, "check-out date is not disabled before check-in date."


@pytest.mark.negative
def test_verify_invalid_city_search_shows_empty_list(load_base_url):
    logger.info("Starting test: test_verify_invalid_city_search_shows_empty_list")
    city_name = yatra_hotel_data["invalid_city_name"]
    select_yatra_service(yatra_common_data["hotels"])
    is_empty_list_displayed = verify_the_invalid_city_search(city_name)
    assert is_empty_list_displayed is True, "Invalid city search did not show an empty list."


@pytest.mark.edge
def test_search_with_max_rooms(driver, load_base_url):
    logger.info("Starting test: test_search_with_max_rooms")
    rooms_to_add = yatra_hotel_data["add_multiple_guests_rooms"]["rooms_index"]
    guests_per_room = yatra_hotel_data["add_multiple_guests_rooms"]["guests_per_room"]
    expected_room_and_guests_info = yatra_hotel_data["add_multiple_guests_rooms"]["expected_room_and_guests_info"]
    select_yatra_service(yatra_common_data["hotels"])
    select_city(driver, yatra_hotel_data["hotels_booking"]["city"])
    actual_room_and_guests_info = select_the_search_with_max_room(driver, rooms_to_add, guests_per_room)
    assert actual_room_and_guests_info == expected_room_and_guests_info, "Selected room and guests info does not match."
    click_search_button()
    assert verify_hotel_search_results_displayed() is True, "Hotel search results are not displayed."


@pytest.mark.edge
def test_checkout_more_than_15_days_after_checkin(load_base_url):
    logger.info("Starting test: test_checkout_more_than_15_days_after_checkin")
    checkout_days = yatra_hotel_data["checkout_more_than_15_days"]["check_out_after_days"]
    checkout_calendar = yatra_hotel_data["checkout_calendar"] 
    error_msg = yatra_hotel_data["checkout_more_than_15_days"]["expected_error_message"]
    select_yatra_service(yatra_common_data["hotels"])
    is_true = get_more_than_15_days_checkout_error_message(checkout_days, checkout_calendar, error_msg)  # Check-out date: 31 days from today
    logger.info(f"Error message displayed: {is_true}")
    assert is_true is True, "Expected error message not displayed for more than 15 days checkout after check-in." 


@pytest.mark.positive
def test_fill_form_and_verify_rent_on_payment_page(load_base_url):
    logger.info("Starting test: test_fill_form_and_verify_rent_on_payment_page")
    select_yatra_service(yatra_common_data["hotels"])
    remove_room_and_guest_selection()
    click_search_button()
    total_rent_on_review_page = choose_room_and_get_the_rent_on_review_page()
    total_rent_on_payment_page = fill_review_page_form_and_get_the_rent_on_payment_page()
    assert int(total_rent_on_payment_page.replace(',', '')) == int(total_rent_on_review_page.replace(',', '')), "Total rent on payment page does not match expected rent."


@pytest.mark.positive
def test_apply_coupan_and_verify_discount_on_review_page(load_base_url):
    logger.info("Starting test: test_apply_coupan_and_verify_discount_on_review_page")
    select_yatra_service(yatra_common_data["hotels"])
    click_search_button()
    total_rent_before_discount = choose_room_and_get_the_rent_on_review_page(remove_coupan=True)
    discount_amount = apply_coupan_and_get_discount_on_review_page()
    expected_rent_after_discount = int(total_rent_before_discount.replace(',', '')) - int(discount_amount.replace(',', ''))
    logger.info(f"Expected rent after discount: {expected_rent_after_discount}")
    actual_rent_after_discount = get_total_rent_after_discount_on_review_page(total_rent_before_discount)
    assert expected_rent_after_discount == int(actual_rent_after_discount.replace(',', '')), "Total rent after applying coupon does not match expected rent."


@pytest.mark.negative
def test_verify_invalid_email_error_on_review_page_form(load_base_url):
    logger.info("Starting test: test_verify_invalid_email_error_on_review_page_form")
    field_name = yatra_hotel_data["field_name_email"]
    invalid_email = yatra_hotel_data["invalid_email"]
    expected_error_msg = yatra_hotel_data["invalid_email_msg"]
    select_yatra_service(yatra_common_data["hotels"])
    click_search_button()
    choose_room_and_get_the_rent_on_review_page()
    actual_error_msg = fill_invalid_detail_in_form(invalid_email, field_name)
    assert actual_error_msg == expected_error_msg, "Invalid email error message does not match expected message."


@pytest.mark.negative
def test_verify_incomplete_phone_number_error_on_review_page_form(load_base_url):
    logger.info("Starting test: test_verify_incomplete_phone_number_error_on_review_page_form")
    field_name = yatra_hotel_data["field_name_phone"]
    incomplete_phone = yatra_hotel_data["incomplete_phone"]
    expected_error_msg = yatra_hotel_data["incomplete_phone_msg"]
    select_yatra_service(yatra_common_data["hotels"])
    click_search_button()
    choose_room_and_get_the_rent_on_review_page()
    actual_error_msg = fill_invalid_detail_in_form(incomplete_phone, field_name)
    assert actual_error_msg == expected_error_msg, "Incomplete phone number error message does not match expected message."


@pytest.mark.edge
def test_verify_invalid_credit_card_number_error_on_payment_page(load_base_url):
    logger.info("Starting test: test_verify_invalid_credit_card_number_error_on_payment_page")
    credit_card_details = yatra_hotel_data["credit_card_details"]
    select_yatra_service(yatra_common_data["hotels"])
    remove_room_and_guest_selection()
    click_search_button()
    choose_room_and_get_the_rent_on_review_page()
    fill_review_page_form_and_get_the_rent_on_payment_page()
    is_error_msg_present = fill_credit_card_details_and_get_invalid_card_error(credit_card_details)
    assert is_error_msg_present == True, "Invalid credit card number error message does not match expected message."
