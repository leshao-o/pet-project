# ruff: noqa: F405
from src.repositories.mappers.base import DataMapper
from src.models import *  # noqa
from src.schemas import *  # noqa


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class UserDataWithHashedPasswordMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility
