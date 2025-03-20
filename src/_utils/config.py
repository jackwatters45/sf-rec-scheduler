from typing import TypedDict, Literal
from src._utils.date_utils import Weekday
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class DesiredDateTime(TypedDict):
    weekday: Weekday
    time: str
    frequency: Literal["WEEKLY", "DAILY"]


def validate_weekday_and_frequency(
    weekday: str,
    frequency: str,
    default_weekday: str = "WEDNESDAY",
    default_frequency: str = "WEEKLY",
) -> tuple[str, str]:
    """Validate weekday and frequency values.

    Args:
        weekday: The weekday to validate
        frequency: The frequency to validate
        default_weekday: Default weekday if validation fails
        default_frequency: Default frequency if validation fails

    Returns:
        tuple[str, str]: Validated weekday and frequency
    """
    valid_weekdays = [
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY",
    ]
    valid_frequencies = ["WEEKLY", "DAILY"]

    if weekday not in valid_weekdays:
        weekday = default_weekday
    if frequency not in valid_frequencies:
        frequency = default_frequency

    return weekday, frequency


def get_desired_date_time() -> DesiredDateTime:
    """Get reservation date/time settings from environment variables."""
    weekday = os.getenv("DESIRED_WEEKDAY", "WEDNESDAY")
    time = os.getenv("DESIRED_TIME", "20:00")
    frequency = os.getenv("RESERVATION_FREQUENCY", "WEEKLY")

    # Validate the values
    weekday, frequency = validate_weekday_and_frequency(
        weekday=weekday,
        frequency=frequency,
        default_weekday="WEDNESDAY",
        default_frequency="WEEKLY",
    )

    return {
        "weekday": weekday,  # type: ignore
        "time": time,
        "frequency": frequency,  # type: ignore
    }


def validate_schedule_settings() -> tuple[str, str, str]:
    """Validate and return schedule settings."""
    weekday = os.getenv("SCHEDULE_WEEKDAY", "MONDAY")
    time = os.getenv("SCHEDULE_TIME", "09:00")
    frequency = os.getenv("SCHEDULE_FREQUENCY", "WEEKLY")

    # Validate the values
    weekday, frequency = validate_weekday_and_frequency(
        weekday=weekday,
        frequency=frequency,
        default_weekday="MONDAY",
        default_frequency="WEEKLY",
    )

    return weekday, time, frequency


# Reservation Settings
DESIRED_DATE_TIME = get_desired_date_time()

# Time Preferences
DESIRED_TIME_MILITARY = os.getenv("DESIRED_TIME_MILITARY", "20:00:00")
ALT_DESIRED_TIMES_MILITARY = os.getenv(
    "ALT_DESIRED_TIMES_MILITARY", "19:00:00,21:00:00"
).split(",")

# Field Preferences
DESIRED_FIELD_STARTS_WITH = os.getenv("DESIRED_FIELD_STARTS_WITH", "FIELD - Main")
FACILITY_GROUP_ID = int(os.getenv("FACILITY_GROUP_ID", "28"))

# Activity Settings
SPORT = os.getenv("SPORT", "Soccer")
RESERVATION_NAME = os.getenv("RESERVATION_NAME", "Local Sports Club Practice")
QUANTITY = int(os.getenv("QUANTITY", "20"))

# Deployment Settings
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# Payment Settings
CVV = os.getenv("CVV", "")  # Default to empty string if not set
if not CVV:
    raise ValueError("CVV environment variable is not set")

# Scheduling Settings
SCHEDULE_WEEKDAY, SCHEDULE_TIME, SCHEDULE_FREQUENCY = validate_schedule_settings()
