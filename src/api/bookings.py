from fastapi import Body, APIRouter

from src.services.bookings import BookingService
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
)
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "",
    summary="Получение бронирований",
    description="Получение всех бронирований во всех отелях",
)
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="Получение всех бронирований текущего залогиненного пользователя",
)
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_user_bookings(user_id)


@router.post(
    "",
    summary="Создание бронирования",
    description="Создание нового бронирования для пользователя",
)
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest = Body()):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
