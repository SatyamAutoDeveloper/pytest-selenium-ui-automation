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
    verify_hotel_search_results_displayed()