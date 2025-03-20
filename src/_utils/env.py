from dotenv import load_dotenv
import os
from typing import NamedTuple


class Credentials(NamedTuple):
    email: str
    password: str


def load_credentials() -> Credentials:
    """Load and validate SF Rec credentials from environment variables."""
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    email = os.getenv("SF_REC_EMAIL")
    password = os.getenv("SF_REC_PASSWORD")

    if not email or not password:
        raise ValueError("SF_REC_EMAIL and SF_REC_PASSWORD must be set in .env file")

    return Credentials(email=email, password=password)
