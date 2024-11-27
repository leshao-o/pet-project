from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, facilities_data: FacilityAdd):
        facility = await self.db.facilities.add(facilities_data)
        await self.db.commit()
        test_task.delay()
        return facility

    async def get_all_facilities(self):
        return await self.db.facilities.get_all()
