from datetime import datetime, timedelta
import schedule
from src._utils.logger import setup_logger
import time

logger = setup_logger()


def test_scheduler() -> None:
    """Test the scheduler by simulating a job run a few minutes from now."""
    # Calculate time 2 minutes from now
    now = datetime.now()
    test_time = now + timedelta(minutes=2)
    test_time_str = test_time.strftime("%H:%M")

    def test_job() -> None:
        """Simulate the job by just logging."""
        logger.info("Test job executed successfully!")

    logger.info(f"Testing scheduler - job will run at {test_time_str}")
    schedule.every().day.at(test_time_str).do(test_job)  # type: ignore

    # Run the scheduler for 3 minutes
    end_time = now + timedelta(minutes=3)
    while datetime.now() < end_time:
        schedule.run_pending()
        time.sleep(1)
