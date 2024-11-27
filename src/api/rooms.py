from datetime import date
from fastapi import Body, APIRouter, Query

from src.services.rooms import RoomService
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение комнат",
    description="Получение свободных комнат на определенные даты в конкретном отеле",
)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_rooms(hotel_id, date_from, date_to)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение комнаты",
    description="Получение конкретной комнаты в конкретном отеле",
)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post(
    "/{hotel_id}/rooms",
    summary="Создание комнат",
    description="Создание новой комнаты в конкретном отеле",
)
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "lux",
                "value": {
                    "title": "Улучшенный с террасой и видом на озеро",
                    "description": "Невероятный красоты номер.",
                    "price": 24500,
                    "quantity": 3,
                    "facilities_ids": [1, 2, 3, 4],
                },
            },
            "2": {
                "summary": "super lux",
                "value": {
                    "title": "Делюкс Плюс",
                    "description": "Лучший номер отеля.",
                    "price": 22450,
                    "quantity": 10,
                    "facilities_ids": [1, 2, 3, 4],
                },
            },
            "3": {
                "summary": "for two",
                "value": {
                    "title": "Номер на 2-х человек",
                    "description": "Красота неописуемая.",
                    "price": 4570,
                    "quantity": 15,
                    "facilities_ids": [2, 3],
                },
            },
            "4": {
                "summary": "for three",
                "value": {
                    "title": "Номер на 3-х человек",
                    "description": None,
                    "price": 4350,
                    "quantity": 8,
                    "facilities_ids": [1, 3],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление комнаты",
    description="Удаление комнаты в конкретном отеле",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}


@router.put(
    "/{hotel_id}/rooms",
    summary="Изменение комнаты",
    description="Изменение данных о комнате в конкретном отеле",
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest = Body()):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное изменение комнаты",
    description="Частичное изменение данных о комнате в конкретном отеле",
)
async def change_room_partially(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    await RoomService(db).change_room_partially(hotel_id, room_id, room_data)
    return {"status": "OK"}
