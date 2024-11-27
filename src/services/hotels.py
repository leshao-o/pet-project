from datetime import date

from src.schemas.hotels import HotelAdd
from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    check_date_to_after_date_from,
)
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=(pagination.per_page),
            offset=(pagination.per_page * (pagination.page - 1)),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def get_check_hotel_existance(self, hotel_id):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
