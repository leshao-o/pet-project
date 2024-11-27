from fastapi import Body, APIRouter
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "",
    summary="Получение удобств",
    description="Получение списка всех удобств которые есть",
)
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post(
    "",
    summary="Создание нового удобства",
    description="Создание нового удобства в отелях",
)
async def create_facility(
    db: DBDep,
    facilities_data: FacilityAdd = Body(
        openapi_examples={
            "1": {"summary": "WI-FI", "value": {"title": "WI-FI"}},
            "2": {"summary": "hair dryer", "value": {"title": "hair dryer"}},
            "3": {"summary": "breakfast", "value": {"title": "breakfast"}},
            "4": {"summary": "SPA", "value": {"title": "SPA"}},
        }
    ),
):
    facility = await FacilityService(db).create_facility(facilities_data)
    return {"status": "OK", "data": facility}
