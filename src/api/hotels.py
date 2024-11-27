from datetime import date
from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.services.hotels import HotelService
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных об отелях",
    description="Получение данных обо всех отелях постранично (с пагинацией)",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
    location: str | None = Query(default=None, description="Местоположение"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    return await HotelService(db).get_hotels(
        pagination,
        date_from,
        date_to,
        location,
        title,
    )


@router.get(
    "{hotel_id}",
    summary="Получение данных об отеле",
    description="Получение данных об только одном отеле если он существует",
)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post(
    "",
    summary="Создание нового отеля",
    description="Создание нового отеля. Нужно location и title",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "sochi",
                "value": {"title": "otel 5 zvezd u morya", "location": "сочи, ул. моря 1"},
            },
            "2": {
                "summary": "dubai",
                "value": {"title": "otel u fontana", "location": "дубай, ул. шейха 2"},
            },
            "3": {
                "summary": "moscow",
                "value": {"title": "otel u red square", "location": "москва, ул. театральная 3"},
            },
            "4": {
                "summary": "seoul",
                "value": {"title": "otel u river Han", "location": "сеул, ул. корейская 4"},
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete(
    "",
    summary="Удаление данных об отеле",
    description="Полное удаление данных об отеле",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put(
    "",
    summary="изменение данных об отеле",
    description="Изменение данных об отеле. Меняется location и title",
)
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "sochi",
                "value": {"title": "otel 3 zvezdi u cafe", "location": "сочи, ул. кофе 8"},
            },
            "2": {
                "summary": "dubai",
                "value": {"title": "otel u beach", "location": "дубай, ул. пляжная 4"},
            },
            "3": {
                "summary": "moscow",
                "value": {"title": "otel u white square", "location": "москва, ул. охотный ряд 9"},
            },
            "4": {
                "summary": "seoul",
                "value": {"title": "otel u bts office", "location": "сеул, ул. звездная 10"},
            },
        }
    ),
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное изменений данных об отеле",
    description="Изменение данных об отеле: можно location, можно title",
)
async def change_hotel_partially(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}
