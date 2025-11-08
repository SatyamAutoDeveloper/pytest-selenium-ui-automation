import datetime
import logging

logger = logging.getLogger(__name__)

def get_day_suffix(day):
    """Returns the ordinal suffix (st, nd, rd, th) for a day number."""
    if 11 <= day <= 13:
        return 'th'
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    return suffixes.get(day % 10, 'th')

def get_tomorrow_date():
    """
    Returns tomorrow's date formatted for use in a web locator.
    Returns:
        str: Formatted date string for tomorrow (e.g., "Choose Sunday, November 2nd, 2025") 
    """
    # 1. Get the current date (date object)
    today = datetime.date.today()

    # 2. Calculate tomorrow's date by adding a timedelta of 1 day
    tomorrow = today + datetime.timedelta(days=1)

    # 3. Format tomorrow's date for use in the given XPath locator
    
    # Get the day number (e.g., 2) and append the suffix (e.g., 'nd')
    day_with_suffix = str(tomorrow.day) + get_day_suffix(tomorrow.day)
    
    # Use strftime to format the rest of the date components: 
    # %A = Full weekday name (e.g., Sunday)
    # %B = Full month name (e.g., November)
    # %Y = Year (e.g., 2025)
    date_format = tomorrow.strftime(f"Choose %A, %B {day_with_suffix}, %Y")
    return date_format