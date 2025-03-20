import schedule
import time
from src._utils.logger import setup_logger
from src._utils.config import SCHEDULE_WEEKDAY, SCHEDULE_TIME, SCHEDULE_FREQUENCY
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
    # Schedule the job
    if SCHEDULE_FREQUENCY == "WEEKLY":
        weekday_method = getattr(schedule.every(), SCHEDULE_WEEKDAY.lower())
        weekday_method.at(SCHEDULE_TIME).do(job)  # type: ignore
        logger.info(f"Scheduled job to run every {SCHEDULE_WEEKDAY} at {SCHEDULE_TIME}")
    else:  # DAILY
        schedule.every().day.at(SCHEDULE_TIME).do(job)  # type: ignore
        logger.info(f"Scheduled job to run daily at {SCHEDULE_TIME}")

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
