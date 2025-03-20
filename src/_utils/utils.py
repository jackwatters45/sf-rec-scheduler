from datetime import datetime
from re import Pattern
from playwright.sync_api import Page


# Formatting
def military_to_american(military_time: str) -> str:
    """Convert military time (HH:MM:SS) to American time (H:MM AM/PM)"""
    time_obj = datetime.strptime(military_time, "%H:%M:%S")
    return time_obj.strftime("%-I:%M %p")


def american_to_military(american_time: str) -> str:
    """Convert American time (H:MM AM/PM) to military time (HH:MM:SS)"""
    time_obj = datetime.strptime(american_time, "%I:%M %p")
    return time_obj.strftime("%H:%M:%S")


def format_date_for_calendar(date_str: str) -> str:
    """Convert date from YYYY-MM-DD to MMM DD, YYYY format"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%b %d, %Y")


# Extractions
def get_customer_id(page: Page) -> int:
    """
    Gets the customer ID from the login page by searching through the Redux state structure.

    Args:
        page (Page): Playwright page object

    Returns:
        int: The customer ID from the user's account

    Raises:
        ValueError: If the customer ID cannot be found
    """
    nodes = page.evaluate("window.__reduxInitialState")["loginUser"]["_root"][
        "entries"
    ][0][1]["_root"]["nodes"]

    for node in nodes:
        if "entry" in node and node["entry"][0] == "customerid":
            return node["entry"][1]

    raise ValueError("Could not find customer ID in page state")


# Adjust quantity
def adjust_quantity(page: Page, timeslot_selector: Pattern[str], quantity: int) -> None:
    """
    Adjusts the quantity of people for the selected field and time.

    Args:
        page (Page): Playwright page object
        selected_field (FieldInfo): The selected field information
        selected_time (str): The selected time slot
    """

    field_cell = page.get_by_label(timeslot_selector)
    table_header = field_cell.locator("..").locator("..")

    quantity_stepper = table_header.locator("input")
    quantity_stepper.fill(str(quantity))

    page.wait_for_timeout(1000)
