from datetime import datetime, timedelta
import logging
import json
from peewee import *
import ast

from booking_engine.utility.database_models import db, Hotels


def get_room_availability(check_in, nights, adults, children, infants):
    """Function to return the available rooms for the time slot and capacity given by end user.

    Args:
        check_in (str): The check in date
        nights (int): How many nights the user wishes to stay
        adults (int): Number of adults staying in each room
        children (int): Number of children staying in each room
        infants (int): Number of infants staying in each room
    """

    try:
        check_in_dt = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_dt = check_in_dt + timedelta(days=nights)
        current_month = datetime.now().strftime("%B").lower()
        raw_query = """
        SELECT r.*, h.name as hotel_name
        FROM rooms r
        left join hotels h on r.hotel_id = h.id
        WHERE r.adults >= {adults}
        AND r.children >= {children}
        AND r.infants >= {infants}
        AND r.available = true
        AND NOT EXISTS (
            SELECT 1
            FROM reservations res
            WHERE res.room_id = r.id
            AND (
                (res.check_in < '{check_out_dt}' AND res.check_out > '{check_in_dt}')
            )
            AND res.status NOT IN ('cancelled')
        )
        """.format(
            adults=adults,
            children=children,
            infants=infants,
            check_out_dt=str(check_out_dt),
            check_in_dt=str(check_in_dt),
        )
        cursor = db.execute_sql(raw_query)
        # Fetch the cursor description to get column names
        columns = [column[0] for column in cursor.description]
        # Construct a list of dictionaries using column names
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for i in results:
            if i.get("photo_paths"):
                # make photos string into list
                i["photo_paths"] = ast.literal_eval(i["photo_paths"])
            # get price according to month
            i["base_price"] = __get_current_room_price(
                i.get("hotel_id"), i.get("base_price"), current_month
            )
        return results
    except Exception as e:
        logging.error(f"Room availability fetch failed. Exception: {e}")
        return []


def __get_current_room_price(hotel_id, base_price, current_month):
    """Helper function to generate the current price of the room according to the current month. It
    checks the pricing configuration of the hotel and multiplies the base price of the room by the
    multiplier provided in the config.

    Args:
        hotel_id (int): Which hotel ID the room belongs to.
        base_price (int): The base price of the room.
    """
    hotel_info = list(
        Hotels.select(Hotels.seasonal_pricing).where(Hotels.id == hotel_id).dicts()
    )
    if hotel_info:
        hotel_info = hotel_info[0]
    # get the column value
    seasonal_pricing_config = hotel_info.get("seasonal_pricing")
    if seasonal_pricing_config:
        try:
            # replace single quotes with double in order to avoid json error
            config = json.loads(seasonal_pricing_config.replace("'", '"'))
            # if multiplier is found for current month, return the multiplied price, else return base
            multiplier = config.get(current_month)
            if multiplier and (type(multiplier) == int or type(multiplier) == float):
                return int(base_price * config.get(current_month))
            return int(base_price)
        except Exception as e:
            logging.error(
                f"Error loading seasonal pricing config for hotel {hotel_id}. Exception: {e}"
            )
            return int(base_price)
    return int(base_price)
