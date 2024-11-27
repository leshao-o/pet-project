from sqlalchemy import delete, insert, select

from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilityDataMapper

    async def edit_facilities(
        self,
        data: model,
        room_id,
        exclude_unset: bool = False,
    ):
        delete_stmt = delete(self.model).filter_by(room_id=room_id)
        await self.session.execute(delete_stmt)
        insert_stmt = insert(self.model).values(
            [item.model_dump(exclude_unset=exclude_unset) for item in data]
        )
        await self.session.execute(insert_stmt)

    async def set_room_facilities(self, room_id, facilities_ids: list[int]):
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = res.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
