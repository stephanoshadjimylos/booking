from typing import Optional

from pydantic import BaseModel


class ClassGetAvailability(BaseModel):
    check_in: str
    nights: int
    adults: int
    children: Optional[int] = 0
    infants: Optional[int] = 0
