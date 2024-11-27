from pydantic import BaseModel


# модель на добавление
class HotelAdd(BaseModel):
    title: str
    location: str


# модель на чтение
class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
