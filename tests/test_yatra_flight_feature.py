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
    select_departure_date()
    click_search_button()
    logger.info("Verifying that search results are displayed.")
    assert is_search_results_displayed() is True, "Search results are not displayed."