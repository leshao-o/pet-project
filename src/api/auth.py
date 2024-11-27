from fastapi import APIRouter, HTTPException, Response

from src.exceptions import ObjectAlreadyExistException
from src.api.dependencies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя если пользователь с таким email не зарегестрирован",
)
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except ObjectAlreadyExistException:
        raise HTTPException(
            status_code=409, detail="Пользователем с таким email уже зарегестрирован"
        )
    await db.commit()
    return {"status": "OK"}


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизация пользователя если пользователь существует",
)
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=401, detail="Пользователем с таким email не зарегестрирован"
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post(
    "/",
    summary="Разлогинивание пользователя",
    description="Разлогинивание пользователя путем удаления access_token(jwt)",
)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get(
    "/me",
    summary="Получение пользователя",
    description="Получение текущего авторизованного пользователя если авторизованн",
)
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user
