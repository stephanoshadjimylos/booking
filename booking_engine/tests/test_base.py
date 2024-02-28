from booking_engine.utility.database_models import Hotels, Rooms


class TestBase:
    """
    Base class responsible for initiating class variables
    that are inherited by the test files to use as input payloads for the functions being tested.
    """

    hotel_object = list(Hotels.select().dicts())[0]  # hotel row to be used in tests
    room_object = list(Rooms.select().dicts())[0]  # room row to be used in tests
    seasonal_pricing = {
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
