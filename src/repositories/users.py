from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper, UserDataWithHashedPasswordMapper
from src.models.users import UsersORM


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()

        return UserDataWithHashedPasswordMapper.map_to_domain_entity(model)