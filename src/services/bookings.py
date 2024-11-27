from src.services.rooms import RoomService
from src.exceptions import AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService
from src.api.dependencies import UserIdDep


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: UserIdDep, booking_data: BookingAddRequest):
        room = await RoomService(self.db).get_check_room_existance(booking_data.room_id)
        _booking_data = BookingAdd(price=room.price, user_id=user_id, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data)
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking
