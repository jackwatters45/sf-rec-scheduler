from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Literal
from enum import Enum
from zoneinfo import ZoneInfo


load_dotenv()


class Weekday(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


# Map weekdays to their numeric values (0-6)
WEEKDAY_MAP = {
    Weekday.MONDAY: 0,
    Weekday.TUESDAY: 1,
    Weekday.WEDNESDAY: 2,
    Weekday.THURSDAY: 3,
    Weekday.FRIDAY: 4,
    Weekday.SATURDAY: 5,
    Weekday.SUNDAY: 6,
}


class Settings(BaseSettings):
    # Credentials
    sf_rec_email: str
    sf_rec_password: str

    # Reservation Settings
    desired_weekday: Weekday = Weekday.WEDNESDAY
    desired_time_military: str = "20:00:00"
    reservation_frequency: Literal["WEEKLY", "DAILY"] = "WEEKLY"
    alt_desired_times_military: list[str] = ["19:00:00"]
    occurrences_ahead: int = 2

    # Field Preferences
    desired_field_starts_with: str
    facility_group_id: int = 28

    # Activity Settings
    sport: str
    reservation_name: str
    group_quantity: int = 15

    # Deployment Settings
    headless: bool = False
    max_retries: int = 3
    retry_delay: int = 5

    # Payment Settings
    cvv: str

    # Schedule Settings
    schedule_weekday: Weekday = Weekday.WEDNESDAY
    schedule_time: str = "10:00"
    schedule_frequency: Literal["WEEKLY", "DAILY"] = "WEEKLY"
    timezone: str = "America/Los_Angeles"  # Pacific Time

    @property
    def tzinfo(self) -> ZoneInfo:
        """Get the timezone info object."""
        return ZoneInfo(self.timezone)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()  # type: ignore
