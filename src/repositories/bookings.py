from datetime import date
from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_today_bookings_checkin(self):
        query = select(BookingsORM).filter(BookingsORM.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(
        self,
        booking_data: BookingAdd,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from, date_to=booking_data.date_to
        )
        available_rooms_query_result = await self.session.execute(rooms_ids_to_get)
        available_room_ids = available_rooms_query_result.scalars().all()
        if booking_data.room_id in available_room_ids:
            new_booking = await self.add(booking_data)
            return new_booking
        raise AllRoomsAreBookedException
