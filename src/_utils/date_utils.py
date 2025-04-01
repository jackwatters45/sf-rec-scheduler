from datetime import datetime, timedelta
from src._utils.env import Weekday, settings, WEEKDAY_MAP


def get_next_occurrence(weekday: Weekday, time: str) -> str:
    """
    Calculate the next occurrence of a given weekday and time, based on the configured number of occurrences ahead.

    Args:
        weekday (Weekday): The desired day of the week (e.g., "WEDNESDAY")
        time (str): The desired time in 24-hour format (e.g., "20:00")

    Returns:
        str: The date of the next occurrence in YYYY-MM-DD format
    """
    # Get current date
    current_date = datetime.now()

    # Parse the target time
    target_hour, target_minute, _ = map(int, time.split(":"))

    # Get the target weekday number (0-6)
    target_weekday = WEEKDAY_MAP[weekday]

    # Calculate days until next occurrence
    days_ahead = target_weekday - current_date.weekday()
    if days_ahead <= 0:  # If the target day has passed this week
        days_ahead += 7  # Move to next week

    # Add extra weeks based on occurrences_ahead configuration
    # Subtract 1 because we already added one week in the previous step
    days_ahead += 7 * (settings.occurrences_ahead - 1)

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
    return get_next_occurrence(settings.desired_weekday, settings.desired_time_military)


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
    """Convert date from YYYY-MM-DD to MMM DD, YYYY format without leading zeros"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%b %-d, %Y")
