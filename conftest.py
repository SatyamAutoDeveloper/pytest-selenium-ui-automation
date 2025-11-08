import logging
import pathlib
import sys
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from configparser import ConfigParser

# Ensure these imports point to your actual file
from helpers.webdriver_actions import set_driver, clear_driver, load_url, get_driver
from pages.yatra_object import remove_webklipper_iframe

sys.dont_write_bytecode = True
logger = logging.getLogger(__name__)

# --- Configuration Setup ---
# Initialize ConfigParser and read configuration
CONFIG = ConfigParser()
CONFIG.read('config.ini')
# Get base URL, defaulting to a known value
BASE_URL = CONFIG.get('BASE_URL', 'Settings', fallback='https://www.yatra.com')
# Get default reports path (screenshots path is handled by CLI option)
REPORT_PATH_FALLBACK = './reports/'

# --- Helper Functions for WebDriver Setup ---

def _create_webdriver(browser: str, headless: bool) -> webdriver.Remote:
    """
    Initializes and returns a configured WebDriver instance based on browser and headless options.
    """
    if browser == "firefox":
        logger.info("Setting up Firefox WebDriver...")
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = webdriver.firefox.service.Service(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=options)

    elif browser == "chrome":
        logger.info("Setting up Chrome WebDriver (default)...")
        options = ChromeOptions()
        # Use a common, current User-Agent string
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        options.add_argument(f"user-agent={user_agent}")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        if headless:
            # Use "new" for modern Chrome headless mode
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--ignore-certificate-errors')
            # Add flags to hide automation (common bot detection triggers)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # General best practices arguments
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        
        service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=options)
        """Selenium sets a JavaScript property called navigator.webdriver to true. Many bot detection scripts check for this. I need to remove this property immediately after the browser launches."""
        driver_instance.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            }
        )
    
    else:
        raise ValueError(f"Unsupported browser specified: {browser}. Must be 'chrome' or 'firefox'.")

    # Common driver settings
    driver_instance.implicitly_wait(5)
    try:
        if not headless:
            driver_instance.maximize_window()
            logger.info("Browser window maximized.")
    except Exception as e:
        logger.warning(f"Could not maximize window (might be headless or remote): {e}")

    return driver_instance

# --- Pytest Hooks ---
def pytest_addoption(parser):
    """Adds command-line options for browser, headless mode, and screenshot directory."""
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=False, help="run browsers in headless mode")
    parser.addoption("--screenshots-dir", action="store", default="screenshots", help="directory to save failure screenshots")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to attach the report object (rep_call, rep_setup, etc.) to the test item.
    This allows fixtures to inspect the test result, specifically for failure detection.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    # Check if the test failed during the 'call' phase (the actual test execution)
    if report.when == 'call' and report.failed:
        # Access the driver instance from the test function's arguments
        try:
            driver = item.funcargs['driver']
            # 2. Get the screenshot as Base64 encoded PNG
            screenshot_base64 = driver.get_screenshot_as_base64()
            if isinstance(screenshot_base64, bytes):
                screenshot_base64 = screenshot_base64.decode('utf-8')
            # 3. Embed the Base64 image into the HTML report
            # The extras.png method handles embedding a base64 encoded image string
            extra.append(pytest_html.extras.png(screenshot_base64, name="Failure Screenshot"))
            
            # 4. Update the report's extra list
            report.extra = extra

            print("\nScreenshot successfully embedded in HTML report.")
        except KeyError:
            # Handle cases where the 'driver' fixture isn't used
            print("\nWebDriver fixture 'driver' not found for screenshot.")
            return
        except Exception as e:
            print(f"\nFailed to capture screenshot: {e}")
            return

        # Create a unique filename with the test name and a timestamp
        test_name = item.name.replace('/', '_').replace(':', '_') # Clean up name for filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = pathlib.Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True) # Create 'screenshots' directory if it doesn't exist
        
        screenshot_filename = str(screenshot_dir / f"FAIL_{test_name}_{timestamp}.png")
        
        # Take the screenshot
        try:
            driver.save_screenshot(screenshot_filename)
            print(f"\nScreenshot saved: {screenshot_filename}")
        except Exception as e:
            print(f"\nFailed to take screenshot: {e}")


# --- Fixtures ---

@pytest.fixture(scope="session")
def driver(request):
    """
    Creates and manages the WebDriver instance for the entire test session.
    It registers the driver globally and handles screenshot saving on failure
    and proper teardown.
    """
    # 1. Setup: Parse options and configure screenshot directory
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    screenshots_dir = pathlib.Path(request.config.getoption("--screenshots-dir"))
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Driver Creation using helper function
    driver_instance = _create_webdriver(browser, headless)
    
    # 3. Register Driver
    set_driver(driver_instance)
    logger.info("WebDriver instance registered with webdriver_actions.")

    yield driver_instance # Provide the driver to the tests

    # --- Teardown: Runs after all tests using this session fixture are complete ---
    logger.info("Starting WebDriver teardown...")
    clear_driver()
    logger.info("WebDriver instance cleared and browser quit.")

@pytest.fixture(scope="function", autouse=True)
def load_base_url(driver):
    """
    Navigates to the pre-configured base URL before each test function.
    """
    # The 'driver' fixture ensures the instance exists and is registered.
    logger.info(f"Loading base URL: {BASE_URL}")
    time.sleep(2)
    load_url(BASE_URL)
    remove_webklipper_iframe(driver)
    logger.info(f"Current URL after loading base URL: {get_driver().current_url}")


@pytest.fixture(scope="session")
def report_path():
    """
    Ensures the reports directory exists and returns its path.
    """
    path = pathlib.Path(CONFIG.get('report_path', 'Settings', fallback=REPORT_PATH_FALLBACK))
    path.mkdir(parents=True, exist_ok=True)
    return str(path)