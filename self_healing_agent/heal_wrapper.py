from selenium.webdriver.common.by import By
from self_healing_agent.locator_store_helper import LocatorStore
from helpers.webdriver_actions import find_element
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    InvalidSelectorException,
)
from self_healing_agent.ai_healing import OllamaHealer
import logging
import json

logger = logging.getLogger(__name__)


class SmartDriver:
    def __init__(self, driver):
        self.driver = driver
        self.healer = OllamaHealer()
        self.store = LocatorStore()

    def find_element_smart(self, locator, value=None, description=""):
        try:
            return find_element(locator, value)
        except (NoSuchElementException, ElementNotVisibleException):
            # First, check if we have a stored fix
            broken_value = locator[1]
            healed_locator = self.store.get_fix(broken_value)
            if healed_locator:
                logger.info(f"Using stored healed locator for: {broken_value}")
                healed_locator_tuple = (By.XPATH, healed_locator)
                try:
                    return find_element(healed_locator_tuple)
                except (NoSuchElementException, ElementNotVisibleException, InvalidSelectorException):
                    logger.warning(
                        f"Stored healed locator failed for: {broken_value}. Proceeding with AI healing..."
                    )
            else:
                logger.info(f"No cached fix found for: {broken_value}")

            # If no stored fix, use AI to suggest a new locator
            logger.info(
                f"⚠️ No cache found for '{broken_value}'. Healing with Ollama..."
            )
            page_source = self.driver.page_source

            # Get new locator from AI healer
            new_xpath = self.healer.get_healed_locator(
                broken_value, page_source, description
            )
            
            #formatted_xpath = f'"{new_xpath}"'
            # Save the new locator for future use
            logger.info(f"Saving healed locator for: {broken_value} -> {new_xpath}")
            self.store.save_fix(broken_value, new_xpath)
           
            # Attempt to find with the new healed locator (only XPath)
            logger.info(f"💡 Ollama suggested new XPath: {new_xpath}")
            
            ai_healed_locator = (By.XPATH, new_xpath)
            return find_element(ai_healed_locator)
