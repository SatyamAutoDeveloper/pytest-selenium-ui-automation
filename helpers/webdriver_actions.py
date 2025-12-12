import logging
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

logger = logging.getLogger(__name__)

_driver_instance = None


def set_driver(driver):
    """Set the module-level driver (call once from your fixture)."""
    global _driver_instance
    _driver_instance = driver


def get_driver():
    if _driver_instance is None:
        raise RuntimeError(
            "Driver not set. Call set_driver(driver) before using webdriver_actions."
        )
    return _driver_instance


def clear_driver():
    global _driver_instance
    if _driver_instance:  # Check if driver exists before trying to quit
        try:
            _driver_instance.quit()
        except Exception as e:
            logger.error(f"Error quitting driver: {e}")
    _driver_instance = None


def _format_locator(locator, replace_value=None):
    return (
        (locator[0], locator[1].format(replace_value))
        if replace_value is not None
        else locator
    )


def find_element(locator, replace_value=None, shadow_dom=False):
    driver = get_driver()
    formatted_locator = _format_locator(locator, replace_value)
    if shadow_dom:
        # Implement shadow DOM logic if needed
        pass
    return driver.find_element(*formatted_locator)


def find_elements(locator, shadow_dom=False, replace_value=None):
    driver = get_driver()
    formatted_locator = _format_locator(locator, replace_value)
    if shadow_dom:
        # Implement shadow DOM logic if needed
        pass
    return driver.find_elements(*formatted_locator)


def click(locator, replace_value=None, shadow_dom=False, max_retries=3):
    """Click on an element up to max_retries times"""
    for attempt in range(1, max_retries + 1):
        try:
            find_element(locator, replace_value, shadow_dom).click()
            logger.info(f"✅ Successful click on attempt {attempt}.")
            return  # Exit the function if successful

        except (NoSuchElementException, StaleElementReferenceException) as e:
            logger.warning(
                f"⚠️ Attempt {attempt} failed: {type(e).__name__}. Retrying..."
            )
            if attempt < max_retries:
                time.sleep(2)  # Wait 2 seconds before the next retry
            else:
                logger.error(
                    f"❌ All {max_retries} attempts failed for locator: {locator[1], replace_value}"
                )
                raise


def wait_for_element_to_be_visible(
    locator, timeout=10, poll_frequency=0.5, shadow_dom=False, replace_value=None
):
    """Wait until element is visible and return it."""
    formatted_locator = _format_locator(locator, replace_value)
    if shadow_dom:
        end = time.time() + timeout
        while time.time() < end:
            try:
                elem = find_element(locator, replace_value, True)
                if elem.is_displayed():
                    return elem
            except Exception:
                pass
            time.sleep(poll_frequency)
        raise RuntimeError(
            f"Element {formatted_locator} not visible after {timeout} seconds"
        )
    else:
        return WebDriverWait(get_driver(), timeout, poll_frequency).until(
            EC.visibility_of_element_located(formatted_locator)
        )


def select_element_from_dropdown(
    locator, visible_text, shadow_dom=False, replace_value=None
):
    """Select option by visible text from a <select> element located by locator."""
    Select(find_element(locator, replace_value, shadow_dom)).select_by_visible_text(
        visible_text
    )


def implicit_wait(seconds):
    """Set driver implicit wait (affects all find_element calls)."""
    get_driver().implicitly_wait(seconds)


def explicit_wait(
    locator,
    timeout=10,
    poll_frequency=0.5,
    condition="visible",
    shadow_dom=False,
    replace_value=None,
):
    """
    Explicit wait for various conditions.
    condition: 'visible' | 'presence' | 'clickable' | 'invisible'
    Returns element for visible/presence/clickable, True for invisible.
    """
    formatted_locator = _format_locator(locator, replace_value)
    if shadow_dom:
        end = time.time() + timeout
        while time.time() < end:
            try:
                elem = find_element(locator, replace_value, True)
                if condition == "visible" and elem.is_displayed():
                    return elem
                if condition == "presence":
                    return elem
                if (
                    condition == "clickable"
                    and elem.is_displayed()
                    and elem.is_enabled()
                ):
                    return elem
                if condition == "invisible":
                    return not elem.is_displayed()
            except Exception:
                if condition == "invisible":
                    return True
            time.sleep(poll_frequency)
        raise RuntimeError(
            f"Condition '{condition}' not met for {formatted_locator} after {timeout} seconds"
        )
    else:
        wait = WebDriverWait(get_driver(), timeout, poll_frequency)
        conditions = {
            "visible": EC.visibility_of_element_located,
            "presence": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "invisible": EC.invisibility_of_element_located,
        }
        if condition in conditions:
            return wait.until(conditions[condition](formatted_locator))
        raise ValueError(f"Unsupported condition: {condition}")


def wait_for_spinner_off(
    spinner_locator, timeout=15, poll_frequency=0.5, replace_value=None
):
    """Wait until spinner (given by spinner_locator) is not visible/present."""
    formatted_locator = _format_locator(spinner_locator, replace_value)
    return WebDriverWait(get_driver(), timeout, poll_frequency).until(
        EC.invisibility_of_element_located(formatted_locator)
    )


def type_value(locator, text, shadow_dom=False, replace_value=None):
    elem = find_element(locator, replace_value, shadow_dom)
    elem.clear()
    elem.send_keys(text)


def is_element_present(locator, shadow_dom=False, replace_value=None):
    """
    Check if an element is present in the DOM.

    Args:
        locator (str): The locator used to find the element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): A value to replace in the locator if needed. Defaults to None.

    Returns:
        bool: True if the element is present, False otherwise.

    Raises:
        Exception: If the element cannot be found, an exception is raised.
    """
    try:
        find_element(locator, replace_value, shadow_dom)
        return True
    except Exception:
        return False


def is_element_not_present(locator, shadow_dom=False, replace_value=None):
    """
    Check if an element is not present in the DOM.

    Args:
        locator (str): The locator used to find the element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): A value to replace in the locator if needed. Defaults to None.

    Returns:
        bool: True if the element is not present, False otherwise.
    """
    try:
        find_element(locator, replace_value, shadow_dom)
        return False
    except Exception:
        return True


def get_element_text(locator, shadow_dom=False, replace_value=None):
    """
    Retrieves the text content of a web element identified by the given locator.

    Args:
        locator (str): The locator used to find the web element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (str, optional): A value to replace in the text before returning. Defaults to None.

    Returns:
        str: The text content of the web element.
    """
    return find_element(locator, replace_value, shadow_dom).text


def get_elements_text(locator, shadow_dom=False, replace_value=None):
    """
    Return the visible text for all elements found by the given locator.

    Parameters
    ----------
    locator : Any
        The locator used to find elements. Typically a tuple like (By.METHOD, selector)
        or a selector string accepted by the project's find_elements helper.
    shadow_dom : bool, optional
        If True, instruct find_elements to search inside shadow DOM roots where supported.
        Defaults to False.
    replace_value : Any, optional
        Optional value used to replace placeholders in the locator prior to searching
        (useful when locators are templates that require runtime values). Defaults to None.

    Returns
    -------
    list[str]
        A list containing the .text value of each matched element. If no elements are found,
        an empty list is returned.
    """
    return [e.text for e in find_elements(locator, shadow_dom, replace_value)]


def mouse_over_click(locator, shadow_dom=False, replace_value=None):
    """
    Simulates a mouse over action followed by a click on a specified element.

    Args:
        locator (str): The locator for the element to interact with.
        shadow_dom (bool, optional): Indicates whether the element is within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        ElementNotInteractableException: If the element is not interactable at the time of the action.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    ActionChains(get_driver()).move_to_element(elem).click().perform()


def move_to_element(locator, shadow_dom=False, replace_value=None):
    """
    Moves the mouse cursor to the middle of the given element.

    Args:
        locator (tuple): A tuple containing the locator strategy and locator value (e.g., (By.ID, "elementId")).
        shadow_dom (bool, optional): If True, finds element within shadow DOM. Defaults to False.
        replace_value (str, optional): Value to replace in the locator string if using string formatting. Defaults to None.

    Returns:
        None

    Raises:
        TimeoutException: If the element is not found within the timeout period.
        ElementNotInteractableException: If the element is not interactable.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    ActionChains(get_driver()).move_to_element(elem).perform()


def move_to_element_and_click(locator, shadow_dom=False, replace_value=None):
    """
    Moves the mouse cursor to the middle of the given element and performs a click action.

    Args:
        locator (tuple): A tuple containing the locator strategy and locator value (e.g., (By.ID, "elementId")).
        shadow_dom (bool, optional): If True, finds element within shadow DOM. Defaults to False.
        replace_value (str, optional): Value to replace in the locator string if using string formatting. Defaults to None.
    Returns:
        None
    Raises:
        TimeoutException: If the element is not found within the timeout period.
        ElementNotInteractableException: If the element is not interactable.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    ActionChains(get_driver()).move_to_element(elem).click().perform()


def scroll_to_bottom():
    get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_to_top():
    get_driver().execute_script("window.scrollTo(0, 0);")


def scroll_element_into_view(locator, shadow_dom=False, replace_value=None):
    """
    Scrolls the specified element into view within the browser window.

    Args:
        locator (str): The locator used to find the element (e.g., CSS selector, XPath).
        shadow_dom (bool, optional): Indicates whether the element is within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        WebDriverException: If there is an issue executing the JavaScript to scroll the element into view.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    get_driver().execute_script("arguments[0].scrollIntoView(true);", elem)


def refresh_page():
    get_driver().refresh()


def navigate_back():
    get_driver().back()


def navigate_forward():
    get_driver().forward()


def get_current_url():
    try:
        return get_driver().current_url
    except RuntimeError:
        # Driver not set; return empty string instead of raising to avoid errors when called before set_driver.
        return ""


def get_page_title():
    return get_driver().title


def click_via_javascript(locator, shadow_dom=False, replace_value=None):
    """
    Clicks on an element using JavaScript.

    Args:
        locator (str): The locator used to find the element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        WebDriverException: If there is an issue executing the JavaScript to click the element.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    get_driver().execute_script("arguments[0].click();", elem)


def set_element_attribute(locator, attribute_name, attribute_value, shadow_dom=False, replace_value=None):
    """
    Sets an attribute of a web element to a specified value using JavaScript.

    Args:
        locator (str): The locator used to find the web element.
        attribute_name (str): The name of the attribute to set.
        attribute_value (str): The value to set for the attribute.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        WebDriverException: If there is an issue executing the JavaScript to set the attribute.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    get_driver().execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", elem, attribute_name, attribute_value)

def get_element_attribute(locator, attribute_name, shadow_dom=False, replace_value=None):
    """
    Retrieves the value of a specified attribute from a web element using JavaScript.

    Args:
        locator (str): The locator used to find the web element.
        attribute_name (str): The name of the attribute to retrieve.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Returns:
        str: The value of the specified attribute.
    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        WebDriverException: If there is an issue executing the JavaScript to get the attribute.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    return get_driver().execute_script("return arguments[0].getAttribute(arguments[1]);", elem, attribute_name)


def iframe_switch(locator, shadow_dom=False, replace_value=None):
    """
    Switches the driver's context to the specified iframe.

    Args:
        locator (str): The locator used to find the iframe element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the iframe cannot be found using the provided locator.
        WebDriverException: If there is an issue switching to the iframe.
    """
    iframe_elem = find_element(locator, replace_value, shadow_dom)
    get_driver().switch_to.frame(iframe_elem)


def iframe_switch_back():
    """Switches the driver's context back to the default content from an iframe."""
    get_driver().switch_to.default_content()


def accept_alert():
    """Accepts the currently displayed alert."""
    alert = get_driver().switch_to.alert
    alert.accept()


def dismiss_alert():
    """Dismisses the currently displayed alert."""
    alert = get_driver().switch_to.alert
    alert.dismiss()


def get_alert_text():
    """Retrieves the text from the currently displayed alert."""
    alert = get_driver().switch_to.alert
    return alert.text


def send_keys_to_alert(text):
    """Sends keys to the currently displayed alert."""
    alert = get_driver().switch_to.alert
    alert.send_keys(text)


def take_screenshot(file_path):
    """Takes a screenshot of the current browser window and saves it to the specified file path."""
    get_driver().save_screenshot(file_path)


def load_url(url):
    """Loads the specified URL in the browser."""
    get_driver().get(url)


def clear_cookies():
    """Clears all cookies in the current browser session."""
    get_driver().delete_all_cookies()


def is_element_displayed(locator, replace_value=None, shadow_dom=False):
    """
    Check if an element is displayed on the page.

    Args:
        locator (str): The locator used to find the element.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.

    Returns:
        bool: True if the element is displayed, False otherwise.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    return get_driver().execute_script(
        "return arguments[0].offsetParent !== null;", elem
    )


def double_click_on_element(locator, replace_value=None, shadow_dom=False):
    """
    Performs a double-click action on the specified element.

    Args:
        locator (str): The locator used to find the element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        ElementNotInteractableException: If the element is not interactable at the time of the action.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    ActionChains(get_driver()).double_click(elem).perform()


def switch_to_new_tab():
    """Switches the driver's context to the newest browser tab."""
    driver = get_driver()
    logger.info("Switching to the newest browser tab.")
    driver.switch_to.window(driver.window_handles[-1])


def switch_to_original_tab():
    """Switches the driver's context back to the original browser tab."""
    driver = get_driver()
    logger.info("Switching back to the original browser tab.")
    driver.switch_to.window(driver.window_handles[0])


def wait_until_page_ready(timeout=10, poll_frequency=0.5):
    """Waits until the page's readyState is 'complete'."""
    driver = get_driver()
    end_time = time.time() + timeout
    while time.time() < end_time:
        page_state = driver.execute_script("return document.readyState;")
        if page_state == "complete":
            logger.info("Page is fully loaded.")
            return
        time.sleep(poll_frequency)
    raise TimeoutError(f"Page did not reach 'complete' state within {timeout} seconds.")


def scroll_to_center(locator, shadow_dom=False, replace_value=None):
    """
    Scrolls the specified element to the center of the viewport.

    Args:
        locator (str): The locator used to find the element.
        shadow_dom (bool, optional): Indicates whether to search within a shadow DOM. Defaults to False.
        replace_value (any, optional): An optional value to replace in the locator if needed. Defaults to None.

    Raises:
        NoSuchElementException: If the element cannot be found using the provided locator.
        WebDriverException: If there is an issue executing the JavaScript to scroll the element into view.
    """
    elem = find_element(locator, replace_value, shadow_dom)
    get_driver().execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)


def get_elements_count(locator, shadow_dom=False, replace_value=None):
    """
    Returns the count of elements found by the given locator.

    Parameters
    ----------
    locator : Any
        The locator used to find elements. Typically a tuple like (By.METHOD, selector)
        or a selector string accepted by the project's find_elements helper.
    shadow_dom : bool, optional
        If True, instruct find_elements to search inside shadow DOM roots where supported.
        Defaults to False.
    replace_value : Any, optional
        Optional value used to replace placeholders in the locator prior to searching
        (useful when locators are templates that require runtime values). Defaults to None.

    Returns
    -------
    int
        The count of elements found by the locator. Returns 0 if no elements are found.
    """
    return len(find_elements(locator, shadow_dom, replace_value))