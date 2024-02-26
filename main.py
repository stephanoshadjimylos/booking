import sys
import logging

from booking_engine.utility.initiate_functions import initiate_db
from booking_engine.routers.api_v1.routes import initiate_app


if __name__ == "__main__":
    try:
        initiate_db()
        initiate_app()
    except Exception as e:
        logging.error(f"Exception occured on application startup. Exception: {e}")
        sys.exit()
