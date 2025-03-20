import logging
import sys
from typing import Optional


def setup_logger(name: str = "sf_rec", level: Optional[int] = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting and output.

    Args:
        name (str): Name of the logger
        level (Optional[int]): Logging level (defaults to INFO)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only add handlers if the logger doesn't already have them
    if not logger.handlers:
        logger.setLevel(level or logging.INFO)

        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger
