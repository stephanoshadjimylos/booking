from dotenv import load_dotenv

import os

load_dotenv(
    override=True
)  # always override system variables and take only variable from .env


POPULATE_DUMMY_HOTEL_DATA = os.environ.get("POPULATE_DUMMY_HOTEL_DATA", False)
