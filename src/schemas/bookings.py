from datetime import date

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int