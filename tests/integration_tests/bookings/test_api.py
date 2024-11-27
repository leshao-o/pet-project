import pytest
from tests.conftest import get_db_null_pool


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 409),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "room_id, date_from, date_to, bookings_quantity",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-01", "2024-08-10", 2),
        (1, "2024-08-01", "2024-08-10", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    bookings_quantity,
    delete_all_bookings,
    authenticated_ac,
):
    await authenticated_ac.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert bookings_quantity == len(response_my_bookings.json())
