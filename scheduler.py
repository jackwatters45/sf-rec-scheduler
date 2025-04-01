import schedule
import time
from src._utils.logger import setup_logger
from src._utils.env import settings
from src._utils.test_utils import test_scheduler
from main import main

logger = setup_logger()


def job() -> None:
    """Run the reservation bot."""
    try:
        logger.info("Starting reservation bot...")
        main()
        logger.info("Reservation bot completed successfully")
    except Exception as e:
        logger.error(f"Error in reservation bot: {e}")


def run_scheduler() -> None:
    """Set up and run the scheduler."""
    # Parse the schedule time
    schedule_hour, schedule_minute = map(int, settings.schedule_time.split(":"))

    # Schedule the job
    if settings.schedule_frequency == "WEEKLY":
        # Get the weekday method (e.g., schedule.every().wednesday)
        weekday_method = getattr(schedule.every(), settings.schedule_weekday.lower())
        # Schedule the job at the specified time
        weekday_method.at(f"{schedule_hour:02d}:{schedule_minute:02d}").do(job)  # type: ignore
        logger.info(
            f"Scheduled job to run every {settings.schedule_weekday} at {settings.schedule_time} {settings.timezone}"
        )
    else:  # DAILY
        schedule.every().day.at(f"{schedule_hour:02d}:{schedule_minute:02d}").do(job)  # type: ignore
        logger.info(
            f"Scheduled job to run daily at {settings.schedule_time} {settings.timezone}"
        )

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_scheduler()
    else:
        run_scheduler()
