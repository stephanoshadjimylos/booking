from booking_engine.tests.test_base import TestBase
from booking_engine.utility.database_models import Reservations
from booking_engine.utility.reservation_calculator import get_room_availability

import pytest
from datetime import datetime


class TestAvailability(TestBase):

    @pytest.fixture
    def setup_and_teardown(self):
        """Setup / Teardown function to setup the DB rows for each test case and delete the data
        from DB on teardown

        Yields:
            int: The reservation ID
        """
        reservation = Reservations.insert(
            room_id=self.room_object.get("id"),
            check_in=datetime(2024, 2, 1, 0, 0, 0),
            check_out=datetime(2024, 2, 3, 0, 0, 0),
            status="confirmed",
        ).execute()
        yield reservation
        Reservations.delete().execute()

    @pytest.mark.parametrize(
        "check_in, nights, adults, children, infants, expected_result",
        [
            ("2024-02-01", 2, 2, 0, 0, []),  # exactly the dates of reservation
            (
                "2024-02-01",
                1,
                2,
                0,
                0,
                [],
            ),  # one night inside the range of the reservation
            (
                "2024-02-02",
                1,
                2,
                0,
                0,
                [],
            ),  # one night inside the range of the reservation
            ("2024-02-02", 1, 2, 1, 0, []),  # one night with children > 0
            ("2024-02-02", 1, 2, 0, 1, []),  # one night with infants > 0
        ],
    )
    def test_no_availability(
        self,
        setup_and_teardown,
        check_in,
        nights,
        adults,
        children,
        infants,
        expected_result,
    ):
        """Test to see that availability return False correctly."""
        res = get_room_availability(check_in, nights, adults, children, infants)
        assert res == expected_result

    @pytest.mark.parametrize(
        "check_in, nights, adults, children, infants",
        [
            (
                "2024-02-05",
                2,
                2,
                0,
                0,
            ),  # date in the month that has nothing to do with reservation
            (
                "2024-01-30",
                2,
                2,
                0,
                0,
            ),  # date finishing on the check_in of the existing reservation
            (
                "2024-02-03",
                2,
                2,
                0,
                0,
            ),  # date starting on the check_out of the existing reservation
        ],
    )
    def test_availability(
        self, setup_and_teardown, check_in, nights, adults, children, infants
    ):
        """Test to see that availability return True correctly."""
        res = get_room_availability(check_in, nights, adults, children, infants)
        assert len(res) > 0
        assert res[0].get("id") == 1
        assert res[0].get("hotel_id") == 1
        assert res[0].get("name") == "Test Room"

    def test_correct_price(self, setup_and_teardown):
        """Test to see that correct price/night is returned."""
        current_month = datetime.now().strftime("%B").lower()
        multiplier = self.seasonal_pricing.get(current_month)
        room_base_price = self.room_object.get("base_price")
        expected_price = room_base_price * multiplier
        res = get_room_availability("2024-02-05", 2, 2, 0, 0)
        assert res[0].get("base_price") == expected_price
