# ruff: noqa: E402
import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **krwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *  # noqa
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


# unset MODE DB_NAME DB_HOST DB_PORT DB_USER DB_PASS REDIS_HOST REDIS_PORT JWT_SECRET_KEY JWT_ALGORITHM ACCESS_TOKEN_EXPIRE_MINUTES


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


# перезаписываем/перегружаем зависимость чтобы для запроса в api
# использовался engine с null_pool
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def db():
    async for db in get_db_null_pool():
        yield db


def get_data_from_json(path):
    with open(path, "r") as file:
        data = json.loads(file.read())
    return data


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_test_database_info(setup_database):
    hotels_data = get_data_from_json("tests/mock_hotels.json")
    rooms_data = get_data_from_json("tests/mock_rooms.json")
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(url="/auth/register", json={"email": "qwerty@test.com", "password": "123456"})


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(url="/auth/login", json={"email": "qwerty@test.com", "password": "123456"})
    assert ac.cookies["access_token"]
    yield ac
