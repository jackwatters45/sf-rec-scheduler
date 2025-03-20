from datetime import datetime, timedelta
from typing import Literal
import src._utils.config as config


Weekday = Literal[
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"
]

WEEKDAY_MAP = {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2,
    "THURSDAY": 3,
    "FRIDAY": 4,
    "SATURDAY": 5,
    "SUNDAY": 6,
}


def get_next_occurrence(weekday: Weekday, time: str) -> str:
    """
    Calculate the next occurrence of a given weekday and time.

    Args:
        weekday (Weekday): The desired day of the week (e.g., "WEDNESDAY")
        time (str): The desired time in 24-hour format (e.g., "20:00")

    Returns:
        str: The date of the next occurrence in YYYY-MM-DD format
    """
    # Get current date
    current_date = datetime.now()

    # Parse the target time
    target_hour, target_minute = map(int, time.split(":"))

    # Get the target weekday number (0-6)
    target_weekday = WEEKDAY_MAP[weekday]

    # Calculate days until next occurrence
    days_ahead = target_weekday - current_date.weekday()
    if days_ahead <= 0:  # If the target day has passed this week
        days_ahead += 7  # Move to next week

    # Calculate the target date
    target_date = current_date + timedelta(days=days_ahead)

    # Set the time
    target_date = target_date.replace(
        hour=target_hour, minute=target_minute, second=0, microsecond=0
    )

    # If the calculated time has already passed today, move to next week
    if target_date < current_date:
        target_date += timedelta(days=7)

    return target_date.strftime("%Y-%m-%d")


def calculate_request_date() -> str:
    """
    Calculate the next occurrence of the desired date and time.

    Returns:
        str: The date of the next occurrence in YYYY-MM-DD format
    """
    weekday = config.DESIRED_DATE_TIME["weekday"]
    time = config.DESIRED_DATE_TIME["time"]
    return get_next_occurrence(weekday, time)
