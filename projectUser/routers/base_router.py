from fastapi import APIRouter, Depends, status, Body
from schemas.base_schemas import User, UserCreate, UserUpdate, UserOutputSchemas
from services.users_service import UsersService

router = APIRouter(prefix="/v1/users", tags=["Книги"])

#получения списка книг
@router.get("", status_code=status.HTTP_200_OK,
            summary="Список пользователей", 
            description="Метод возвращает список пользователей", 
            response_model=list[User])

async def get_users(service: UsersService = Depends()):
    return await service.get_users_all()

#создание новой записи
@router.post("/user-create", status_code=status.HTTP_201_CREATED,
            summary="Добавление пользователя", 
            description="Метод создаёт нового пользователя",
            response_model=UserOutputSchemas)

async def create_user(user:UserCreate = Body(), service: UsersService = Depends()):
    return await service.create_user(user)
    
#обновление записи
@router.put("/{user_id}", status_code=status.HTTP_200_OK, 
            summary="Обновление записи", 
            description="Метод обновляет запись пользователя по идентификатору",
            response_model=UserOutputSchemas)

async def update_user(user_id: int, user: UserUpdate, service: UsersService = Depends()):
    return await service.update_user(user_id, user)

#удаление записи
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT, 
            summary="Удаление пользователя", 
            description="Метод удаляет пользователя по идентификатору")

async def delete_user(user_id: int, service: UsersService = Depends()):
    return await service.delete_user(user_id)


