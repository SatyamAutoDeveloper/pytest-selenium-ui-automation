from helpers.page_helpers import *
from helpers.webdriver_actions import *
from locators.yatra_hotel_locators import *
import logging

logger = logging.getLogger(__name__)


def select_city(driver, city_name):
    """Selects the departure and arrival city."""
    city_name_option = (select_hotel_city_list_item[0], select_hotel_city_list_item[1].format(city_name))
    logger.info(f"Selecting the city: {city_name} with option locator: {city_name_option}")
    wait_for_element_to_be_visible(open_hotel_city)
    click(open_hotel_city)
    wait_for_element_to_be_visible(hotel_city_input)
    type_value(hotel_city_input, city_name)
    implicit_wait(5)
    wait_for_element_to_be_visible(select_hotel_city_list_dd_container)
    scroll_element_into_view_in_side_bar(driver, select_hotel_city_list_dd_container, city_name_option)
    click(city_name_option)


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
    scroll_element_into_view(hotel_search_results_section)
    breadcrumb = get_element_text(search_result_breadcrumb)
    logger.info(f"Search Result Breadcrumb: {breadcrumb}")
    available_hotel_text = get_element_text(hotel_search_results_section)
    logger.info(f"Available Hotel Options: {available_hotel_text}")
    return "hotel options available" in available_hotel_text.lower() and "Bangalore" in breadcrumb


def apply_complex_filters_on_hotel_search(driver, localities, theme):
    """Applies complex filters on hotel search results."""
    logger.info("Applying complex filters on hotel search results.")
    localities_elem = (hotel_filter_option[0], hotel_filter_option[1].format(localities))
    theme_elem = (hotel_filter_option[0], hotel_filter_option[1].format(theme))
    scroll_element_into_view_in_side_bar(driver, filters_side_panel, star_5_rating_filter_option)
    click(star_5_rating_filter_option)
    if is_element_present(localities_elem) is False:
        scroll_element_into_view_in_side_bar(driver, filters_side_panel, localities_show_more_btn)
        click(localities_show_more_btn)
    scroll_element_into_view_in_side_bar(driver, filters_side_panel, localities_elem)
    click(localities_elem)
    scroll_element_into_view_in_side_bar(driver, filters_side_panel, theme_elem)
    click(theme_elem)


def verify_applied_filters_on_hotel_search(driver, expected_filters):
    """Verifies that the applied filters are displayed correctly."""
    logger.info("Verifying the applied filters on hotel search results.")
    wait_for_element_to_be_visible(applied_filters_section)
    scroll_element_into_view_in_side_bar(driver, filters_side_panel, applied_filters_section)
    applied_filters = get_elements_text(applied_filters_section)
    logger.info(f"Applied Filters: {applied_filters}")
    for expected_filter in expected_filters:
        if expected_filter not in applied_filters:
            logger.error(f"Expected filter '{expected_filter}' not found in applied filters.")
            return False
    logger.info("All expected filters are correctly applied.")
    return True


def is_checkout_date_disabled_for_invalid_date_selection(invalid_checkout_days, checkout_calendar):
    """Verify checkout date is disabled when selecting before checkin date"""
    is_disabled = select_date(invalid_checkout_days, checkout_calendar)
    logger.info(f"is checkout disabled when selecting before checkin date:: {is_disabled}")
    return is_disabled


def verify_the_invalid_city_search(city_name):
    """Verifies that searching for an invalid city shows an empty list."""
    logger.info("Verifying invalid city search with empty list.")
    wait_for_element_to_be_visible(open_hotel_city)
    click(open_hotel_city)
    wait_for_element_to_be_visible(hotel_city_input)
    type_value(hotel_city_input, city_name)
    implicit_wait(5)
    wait_for_element_to_be_visible(invalid_city_search_with_empty_list)
    is_empty_list_displayed = is_element_present(invalid_city_search_with_empty_list)
    logger.info(f"Is invalid city search with empty list displayed: {is_empty_list_displayed}")
    return is_empty_list_displayed


def select_the_search_with_max_room(driver, rooms_to_add, guests_per_room):
    """Verifies adding multiple rooms and guests."""
    logger.info("Verifying adding multiple rooms and guests.")
    click(open_room_and_guests_btn)
    wait_for_element_to_be_visible(room_and_guests_popup)
    for room in range(1, rooms_to_add + 1, 2):
        if room > 1:
            click(add_room_button)
            logger.info(f"Added room with Index:: {room}")
        adults = guests_per_room.get(str(room))
        if adults:
            select_adults_elem = (select_adults[0], select_adults[1].format(adults, room))
            scroll_element_into_view_in_side_bar(driver, room_and_guests_popup, select_adults_elem)
            click(select_adults_elem)
            logger.info(f"Selected {adults} adults for room index {room}.")
    click(apply_room_and_guest_button)
    logger.info("Applied room and guest selection.")
    actual_room_and_guests_info = get_element_text(selected_room_and_guests_info)
    logger.info(f"Selected Room and Guests Info: {actual_room_and_guests_info}")
    return actual_room_and_guests_info


def get_more_than_15_days_checkout_error_message(checkout_more_than_15_days, checkout_calendar, expected_error_message):
    """gets the error message for 30 days checkout after check-in."""
    logger.info("Getting the error message for 30 days checkout after check-in.")
    select_date(checkout_more_than_15_days, checkout_calendar)
    wait_for_element_to_be_visible(checkout_more_than_15_days_error_message, replace_value=expected_error_message)
    is_error_message_visible = is_element_present(checkout_more_than_15_days_error_message, replace_value=expected_error_message)
    logger.info(f"Error message displayed: {is_error_message_visible}")
    return is_error_message_visible


def choose_room_and_get_the_rent_on_review_page(remove_coupan=False):
    """Chooses a room and return the rent on the review page."""
    logger.info("Choosing a room and get the rent on review page.")
    click(choose_room_btn)
    implicit_wait(5)
    switch_to_new_tab()
    wait_until_page_ready()
    click(book_this_room_btn)
    if remove_coupan:
        logger.info("Removing applied coupon before getting the rent.")
        scroll_to_center(remove_coupan_btn)
        click(remove_coupan_btn)
    wait_for_element_to_be_visible(total_room_rent)
    room_rent_on_review_page = get_element_attribute(total_room_rent, "aria-label").split("Total Amount-")[1].strip()
    logger.info(f"Room Rent on Review Page: {room_rent_on_review_page}")
    return room_rent_on_review_page


def fill_review_page_form_and_get_the_rent_on_payment_page():
    """Fills the review page form with user details and returns the rent on the payment page."""
    logger.info("Filling the review page form.")
    scroll_element_into_view(form_field, replace_value="email")
    type_value(form_field, "john.doe@example.com", replace_value="email")
    type_value(form_field, "9876543210", replace_value="phoneNumber")
    type_value(form_field, "John", replace_value="firstName")
    type_value(form_field, "Doe", replace_value="lastName")
    logger.info("Review page form filled.")
    scroll_element_into_view(proceed_to_payment_btn)
    click(proceed_to_payment_btn)
    logger.info("Proceeded to payment page.")
    wait_for_element_to_be_visible(rent_on_payment_page)
    rent_payment_page = get_element_text(rent_on_payment_page)
    logger.info(f"Rent on Payment Page: {rent_payment_page}")
    return rent_payment_page


def apply_coupan_and_get_discount_on_review_page():
    """Applies a coupon and returns the total rent before discount and discount amount on the review page."""
    logger.info("Applying coupon on review page.")
    scroll_to_center(select_coupan_btn)
    click(select_coupan_btn)
    wait_for_element_to_be_visible(coupan_discount)
    discount_amount = get_element_text(coupan_discount)[6:].strip()
    logger.info(f"Discount Amount: {discount_amount}")
    return discount_amount


def get_total_rent_after_discount_on_review_page(total_rent_before_discount):
    """Gets the total rent after discount on the review page."""
    logger.info("Getting total rent after discount on review page.")
    scroll_to_center(total_room_rent)
    attribute_changed = wait_for_attribute_change(total_room_rent, "aria-label", total_rent_before_discount)
    if not attribute_changed:
        logger.error("Total rent after discount did not update as expected.")
        raise Exception("Total rent after discount did not update as expected.")
    total_rent_after_discount = get_element_attribute(total_room_rent, "aria-label").split("Total Amount-")[1].strip()
    logger.info(f"Total Rent after Discount: {total_rent_after_discount}")
    return total_rent_after_discount