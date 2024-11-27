from datetime import date
from src.schemas.bookings import BookingAdd


async def test_add_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        date_from=date(year=2024, month=10, day=10),
        date_to=date(year=2024, month=10, day=20),
        user_id=user_id,
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    updated_date = date(year=2024, month=10, day=30)
    data = BookingAdd(
        room_id=room_id,
        date_from=date(year=2024, month=10, day=10),
        date_to=updated_date,
        user_id=user_id,
        price=1000,
    )
    await db.bookings.edit(data=data, exclude_unset=True, room_id=room_id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=room_id)
    assert not booking

    await db.commit()
