import os

os.environ["TEST"] = "True"
from booking_engine.utility.initiate_functions import populate_test_data, initiate_db


def pytest_configure(config):
    # Here we can add any code we want to execute
    # before the tests start
    initiate_db()
    populate_test_data()  # create test hotel
