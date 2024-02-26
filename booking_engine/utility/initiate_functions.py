from booking_engine.utility.database_models import (
    db,
    BaseModel,
    Hotels,
    Rooms,
    Reservations,
)
from settings import POPULATE_DUMMY_HOTEL_DATA

import logging
import random
from datetime import datetime
import os

from peewee import IntegrityError

ROOM_NAMES = ["Seaside View", "Mountain View", "Garden View"]


def initiate_db():
    """Function responsible for initializing the database connection and creating the relevant
    tables."""
    try:
        db.connect()
        # a list of all tables (peewee models) to be created
        tables_to_create = BaseModel.__subclasses__()
        db.create_tables(tables_to_create)
        logging.info("Created DB tables")
    except Exception as e:
        raise Exception(f"{e}")
    if POPULATE_DUMMY_HOTEL_DATA and not os.environ.get("TEST"):
        __populate_dummy_data()
    return True


def populate_test_data():
    """Function to create a dummy hotel for the test database, used for the unit tests.
    """
    try:
        hotel_id = Hotels.insert(
            name=f"Hotel Resort Spa",
            description="4 star hotel",
            street="Test Street",
            city="Athens",
            state="Attica",
            postal_code="15125",
            country="Greece",
            amenities=str(["pool", "tennis", "gym", "sauna"]),
            seasonal_pricing={
                "january": 0.5,
                "february": 0.4,
                "march": 0.5,
                "april": 0.6,
                "may": 0.7,
                "june": 1,
                "july": 1.3,
                "august": 1.5,
                "september": 1.1,
                "october": 0.9,
                "november": 0.7,
                "december": 0.6,
            }
        ).execute()
    except IntegrityError:
        logging.info("Hotel Exists")


def __populate_dummy_data():
    """Function responsible for populating the database with dummy hotel, room and reservation data"""
    try:
        hotel_id = Hotels.insert(
            name=f"Hotel Resort Spa",
            description="4 star hotel",
            street="Test Street",
            city="Athens",
            state="Attica",
            postal_code="15125",
            country="Greece",
            amenities=str(["pool", "tennis", "gym", "sauna"]),
            seasonal_pricing={
                "january": 0.5,
                "february": 0.4,
                "march": 0.5,
                "april": 0.6,
                "may": 0.7,
                "june": 1,
                "july": 1.3,
                "august": 1.5,
                "september": 1.1,
                "october": 0.9,
                "november": 0.7,
                "december": 0.6,
            },
            minimum_stay=2,
        ).execute()

        # insert 5 rooms for this hotel
        for i in range(10):
            room_id = Rooms.insert(
                hotel_id=hotel_id,
                name=random.choice(ROOM_NAMES),
                base_price=random.randrange(100, 200, 10),
                adults=random.randint(1, 4),
                children=random.randint(1, 4),
                infants=random.randint(1, 4),
                photo_paths=random.sample(os.listdir("booking_engine/photos"), 3),
            ).execute()
            check_in, check_out = __generate_random_reservation()
            reservation_id = Reservations.insert(
                room_id=room_id,
                check_in=datetime(2024, 2, check_in, 0, 0, 0),
                check_out=datetime(2024, 2, check_out, 0, 0, 0),
                status="confirmed",
            ).execute()
    except IntegrityError:
        logging.info("Hotel Exists")


def __generate_random_reservation():
    """Helper function to generate random dates for the month of February for a 2 night stay."""
    check_in = random.randint(1, 26)
    check_out = check_in + 2
    return check_in, check_out
