from selenium.webdriver.common.by import By
xpath = By.XPATH
css_selector = By.CSS_SELECTOR

yatra_services = (xpath, "//button[@id='simple-tab-{}']")
yatra_popup_close_button = (xpath, "(//img[@alt='cross'])[1]")
flight_way_radio_btn = (xpath, "//input[@value='{}']")
open_flight_input = (xpath, "//p[@title='{}']")
flight_input = (xpath, "//input[@id='input-with-icon-adornment']")
select_city_option = (xpath, "(//span[contains(text(),'{}')])[1]")
date_calendar = (xpath, "//div[@aria-label='Departure Date inputbox']")
departure_date_input = (xpath, "//div[contains(@aria-label,'{}')]")
traveller_class_input = (xpath, "//input[@id='drop-down-input']")
search_flights_button = (xpath, "//button[normalize-space()='Search']")
sorting_options = (xpath, "//div[@class='grid section-sort']")
prices_on_different_days = (xpath, "//div[@class='scroller full-width flex']")
depart_details_section = (xpath, "(//div[contains(@class,'depart-details')])[1]")
arrival_details_section = (xpath, "(//div[contains(@class,'arrival-details text-right')])[1]")
search_results_section = (css_selector, "div.flightItem.border-shadow.pr")