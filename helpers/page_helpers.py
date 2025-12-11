import datetime
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from helpers.webdriver_actions import get_driver, get_element_attribute

logger = logging.getLogger(__name__)


def get_day_suffix(day):
    """Returns the ordinal suffix (st, nd, rd, th) for a day number."""
    if 11 <= day <= 13:
        return "th"
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    return suffixes.get(day % 10, "th")


def get_formatted_date_in_days(days_offset=0):
    """
    Returns a date formatted for use in a web locator, calculated
    dynamically based on a passed argument in days from today.

    Args:
        days_offset (int): The number of days from today.
                           0 is today, 1 is tomorrow, -1 is yesterday.

    Returns:
        str: Formatted date string (e.g., "Choose Sunday, November 2nd, 2025")
    """
    # 1. Get the current date (date object)
    today = datetime.date.today()

    # 2. Calculate the target date by adding a timedelta of days_offset
    target_date = today + datetime.timedelta(days=days_offset)

    # 3. Format the target date

    # Get the day number (e.g., 2) and append the suffix (e.g., 'nd')
    day_with_suffix = str(target_date.day) + get_day_suffix(target_date.day)

    # Use strftime to format the rest of the date components:
    # %A = Full weekday name (e.g., Sunday)
    # %B = Full month name (e.g., November)
    # %Y = Year (e.g., 2025)
    # Note: We use an f-string to inject the day_with_suffix variable
    if days_offset < 0:
        date_format = target_date.strftime(
            f"Not available %A, %B {day_with_suffix}, %Y"
        )
    else:
        date_format = target_date.strftime(f"Choose %A, %B {day_with_suffix}, %Y")

    return date_format


def calculate_x_offset(
    min_val: int,
    max_val: int,
    target_val: int,
    track_width: int,
    slider_handle_width: int,
) -> int:
    """
    Calculates the necessary horizontal pixel offset to move the slider handle
    from the minimum position (left) to the target value.

    Args:
        min_val: The minimum value the slider represents (e.g., 0).
        max_val: The maximum value the slider represents (e.g., 1000).
        target_val: The desired value to set (e.g., 750).
        track_width: The physical width of the slider track in pixels.

    Returns:
        The calculated X-offset (in pixels) for the ActionChains command.
    """
    if not (min_val <= target_val <= max_val):
        raise ValueError(
            f"Target value ({target_val}) must be between min ({min_val}) and max ({max_val})."
        )

    # 1. Calculate the total range of values
    value_range = max_val - min_val

    # 2. Calculate the position of the target value relative to the min value
    target_position_in_value_units = target_val - min_val

    # 3. Calculate the required offset proportion (0.0 to 1.0)
    proportion = target_position_in_value_units / value_range

    current_pixel_position = track_width - slider_handle_width
    target_pixel_position = current_pixel_position * proportion
    x_offset = target_pixel_position - current_pixel_position
    logger.info(
        f"Proportion: {proportion}, Target Pixel Position: {target_pixel_position}, Current Pixel Position: {current_pixel_position}, Initial X-Offset: {x_offset}"
    )

    adjustment_factor = 0.99  # To avoid overshooting due to rounding
    x_offset *= adjustment_factor
    final_offset = int(x_offset)

    print(f"Calculated X-Offset for price {target_val}: {final_offset} pixels")
    return final_offset


def set_horizontal_slider(
    driver, handle_locator, track_width, min_val, max_val, target_val
):
    """
    Locates the slider handle and moves it horizontally using ActionChains.

    Args:
        driver: The Selenium WebDriver instance.
        handle_locator: Tuple containing the By method and the locator string
                        for the slider handle (circle).
        track_width: The physical width of the slider track in pixels.
        min_val: The minimum possible value of the slider.
        max_val: The maximum possible value of the slider.
        target_val: The desired value to set.
    """
    try:
        slider_handle = driver.find_element(*handle_locator)
        slider_handle_width = slider_handle.size["width"]
        logger.info(f"Slider handle width: {slider_handle_width} pixels")

        # Calculate the required pixel displacement
        x_offset = calculate_x_offset(
            min_val, max_val, target_val, track_width, slider_handle_width
        )

        actions = ActionChains(driver)

        # Perform the drag-and-drop action:
        # The drag starts from the current position of the handle and moves
        # by x_offset pixels horizontally (y_offset is 0).
        # NOTE: This assumes the handle is initially positioned at the min_val (leftmost).
        actions.drag_and_drop_by_offset(slider_handle, x_offset, 0).perform()
        logger.info(
            f"Successfully moved slider handle to an offset of {x_offset} pixels."
        )

    except Exception as e:
        logger.error(f"An error occurred while setting the slider: {e}")
        raise


def scroll_element_into_view_in_side_bar(
    driver, sidebar_locator, target_element_locator
):
    """
    Scrolls a sidebar element to bring a target element into view.

    Args:
        driver: The Selenium WebDriver instance.
        sidebar_locator: Tuple containing the By method and locator string for the sidebar.
        target_element_locator: Tuple containing the By method and locator string for the target element.
    """
    try:
        sidebar = driver.find_element(*sidebar_locator)
        target_element = driver.find_element(*target_element_locator)

        ## 2. Execute JavaScript to Scroll the Container

        # The script calculates the exact relative position needed to bring the
        # target element to the top of the scrollable container.
        script = """
        const container = arguments[0];
        const element = arguments[1];
        
        // Calculate the desired scroll position: 
        // Element's top offset - Container's top offset + Container's current scroll position.
        // This calculates the relative position of the element inside the container 
        // and adds it to the current scroll to move to the new position.
        const scrollPosition = element.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop;
        
        // Set the container's scrollTop property
        container.scrollTop = scrollPosition;
        """

        driver.execute_script(script, sidebar, target_element)

        logger.info(f"Scrolled sidebar to bring element into view.")

    except Exception as e:
        logger.error(f"An error occurred while scrolling the sidebar: {e}")
        raise


def wait_for_attribute_change(locator, attribute, old_value, timeout=20, replace_value=None):
    """
    Wait for an element's attribute to change from its old value.

    This function polls an element's attribute until it changes from the specified old value,
    with a configurable timeout. It uses Selenium's WebDriverWait for efficient waiting.

    Args:
        locator (tuple): The locator strategy and value to find the element (e.g., (By.ID, "element_id")).
        attribute (str): The name of the attribute to monitor for changes.
        old_value (str): The expected original value of the attribute to watch for change.
        timeout (int, optional): Maximum time in seconds to wait for the attribute change. Defaults to 20.
        replace_value (str, optional): Value to replace in the attribute if needed. Defaults to None.

    Returns:
        WebElement: The element whose attribute has changed.

    Raises:
        TimeoutException: If the attribute does not change within the specified timeout.
    """
    driver = get_driver()

    def attribute_has_changed(driver):
        # Find the element and get the current attribute value
        current_value = get_element_attribute(locator, attribute, replace_value=replace_value).split("Total Amount-")[1].strip()
        # Return the True if the value is different from the old_value, otherwise False
        return True if current_value != old_value else False

    return WebDriverWait(driver, timeout).until(attribute_has_changed)
