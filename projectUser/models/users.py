from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column

from models import Base

class User(Base):
    __tablename__= 'users'

    id = mapped_column(Integer, primary_key=True, comment='идентификатор пользователя')
    name = mapped_column(String(100), nullable=False, comment='имя пользователя')
    is_active = mapped_column(Boolean, nullable=False, default=True, comment='статус активности пользователя')
    email = mapped_column(String(100), nullable=False, comment='электронная почта пользователя') 
