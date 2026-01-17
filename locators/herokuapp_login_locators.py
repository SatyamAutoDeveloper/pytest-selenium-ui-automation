from selenium.webdriver.common.by import By
xpath = By.XPATH
css_selector = By.CSS_SELECTOR

username = (xpath, "//input[@id='p0']")
password = (xpath, "//input[@id='p1']")
login_button = (xpath, "//button[@type='lgn']")
login_msg = (xpath, "/div[@id='lgn-scs-msg']")