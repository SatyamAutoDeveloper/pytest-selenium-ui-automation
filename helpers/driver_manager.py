from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from configparser import ConfigParser

class DriverManager:
    def __init__(self):
        self._driver = None
        self._config = ConfigParser()
        self._config.read('config.ini')
        self._headless = self._config.getboolean('Browser', 'headless', fallback=False)

    def create_driver(self, browser_type="chrome"):
        """
        Create and return a WebDriver instance
        :param browser_type: Type of browser ("chrome" or "firefox")
        :return: WebDriver instance
        """
        if browser_type.lower() == "chrome":
            options = ChromeOptions()
            if self._headless:
                options.add_argument('--headless')
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        elif browser_type.lower() == "firefox":
            options = FirefoxOptions()
            if self._headless:
                options.add_argument('--headless')
            self._driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        if not self._headless:
            self._driver.maximize_window()
        return self._driver

    def get_driver(self):
        """
        Get the current WebDriver instance
        :return: WebDriver instance
        """
        if not self._driver:
            return self.create_driver()
        return self._driver

    def quit_driver(self):
        """
        Quit the WebDriver instance
        """
        if self._driver:
            self._driver.quit()
            self._driver = None

    

