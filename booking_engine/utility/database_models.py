import peewee as pw
import os

# if this is run for a test environment, create another DB
if os.environ.get("TEST"):
    db_file = "test.db"
else:
    db_file = "booking.db"

db = pw.SqliteDatabase(f"booking_engine/database/{db_file}")


class BaseModel(pw.Model):
    """Base Class to define peewee base model and database connection."""

    class Meta:
        database = db


class Hotels(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    name = pw.CharField(null=False)
    description = pw.CharField(null=True)
    street = pw.CharField(null=True)
    city = pw.CharField(null=False)
    state = pw.CharField(null=True)
    postal_code = pw.CharField(null=True)
    country = pw.CharField(null=False)
    amenities = pw.CharField(null=True)
    seasonal_pricing = pw.CharField(null=True)
    created = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "hotels"
        indexes = (
            (("name", "description", "street", "city", "postal_code", "country"), True),
        )


class Rooms(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    hotel_id = pw.ForeignKeyField(Hotels, to_field="id")
    name = pw.CharField(null=False)
    base_price = pw.IntegerField(null=False)
    adults = pw.IntegerField(null=False)
    children = pw.IntegerField(null=False)
    infants = pw.IntegerField(null=False)
    available = pw.BooleanField(constraints=[pw.SQL("DEFAULT true")])
    photo_paths = pw.CharField(null=True)
    created = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "rooms"


class Reservations(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    room_id = pw.ForeignKeyField(Rooms, to_field="id")
    check_in = pw.DateTimeField(null=False)
    check_out = pw.DateTimeField(null=False)
    created = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated = pw.DateTimeField(constraints=[pw.SQL("DEFAULT CURRENT_TIMESTAMP")])
    status = pw.CharField(null=False)

    class Meta:
        table_name = "reservations"
