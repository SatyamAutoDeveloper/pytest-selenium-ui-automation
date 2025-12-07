from selenium.webdriver.common.by import By
xpath = By.XPATH
css_selector = By.CSS_SELECTOR

open_hotel_city = (css_selector, "button[aria-label='Button']")
hotel_city_input = (css_selector, "input[type='text']")
select_hotel_city_list_item = (xpath, "(//ul[contains(@class, 'SearchList_listing')])[1]")
select_hotel_city_list = (xpath, "//div[contains(@class, 'SearchPanelModal_searchList')]")
open_date_calendar = (xpath, "//div[contains(@class, 'SearchPanel_hotelDetails')]//button[{}]")
select_date_in_calendar = (xpath, "//div[@aria-label='{}']")
calendar_next_btn = (xpath, "(//button//img[@alt='Night Icon'])[4]")
calendar_prev_btn = (xpath, "(//button//img[@alt='Night Icon'])[1]")
search_hotels_button = (css_selector, "button[aria-label='Search']")
hotel_search_results_section = (xpath, "//div[contains(@class, 'HotelList_hotelListingHeader')]//p")