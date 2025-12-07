from selenium.webdriver.common.by import By
xpath = By.XPATH
css_selector = By.CSS_SELECTOR

yatra_services = (xpath, "//button[@id='simple-tab-{}']")
yatra_popup_close_button = (xpath, "(//img[@alt='cross'])[1]")
ads_iframe_img = (xpath, "//iframe[@id='webklipper-publisher-widget-container-notification-frame']")
ads_iframe_close_btn = (css_selector, "button[name='close']")