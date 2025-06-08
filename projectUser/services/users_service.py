from schemas.base_schemas import  User, UserCreate, UserOutputSchemas, UserUpdate
from fastapi import HTTPException, status, Depends
from pydantic import ValidationError
from database import AsyncSession, get_session
from sqlalchemy import select, update
from models.users import User as UserModel

class UsersService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session

    #функция для получения списка активных пользователей
    async def get_users_all(self):
        users = (await self._session.execute(select(UserModel).where(UserModel.is_active == True))).scalars().all()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="В базе данных нет пользователей"
            )
        return users

    #функция для создания новой записи
    async def create_user(self, user: UserCreate) -> UserOutputSchemas:
        new_user = UserModel(**user.dict())
        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)
    
        return UserOutputSchemas(message=f"Пользователь с id = {new_user.id} успешно создан", 
                                     user = User.model_validate(new_user))

    #функция для обновления записи
    async def update_user(self, user_id: int, user: UserUpdate) -> UserOutputSchemas:
        users = await self._session.execute(select(UserModel).where(UserModel.id ==user_id))
        existing_user = users.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"В базе данных пользователь с id = {user_id} не найден"
            )
        
        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user.dict())
        )

        await self._session.commit()
    
        return UserOutputSchemas(message=f"Пользователь с id = {user_id} успешно обновлён", 
                                     user = User.model_validate(existing_user))

    #функция для удаления записи
    async def delete_user(self, user_id: int):

        users = await self._session.execute(select(UserModel).where(UserModel.id ==user_id))
        existing_user = users.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"В базе данных пользователь с id = {user_id} не найден"
            )
        
        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
        )

        await self._session.commit()


