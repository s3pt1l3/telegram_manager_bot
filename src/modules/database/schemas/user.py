from sqlalchemy import sql, Column, BigInteger, Boolean, String, DateTime
from asyncpg import UniqueViolationError
from datetime import datetime

from sqlalchemy.sql.expression import true

from modules.database import database as db


class User(db.BaseModel):
    """
    Класс модели таблицы пользователей бота
    """

    __tablename__ = 'Users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    tag = Column(String(100))
    is_employee = Column(Boolean)
    is_admin = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, tag: str, is_admin: bool=False, is_employee: bool=False):
    """
    Функция для добавления пользователя в бд

    `user_id`: ID пользователя в Telegram\n
    `tag`: Тэг пользователя в Telegram\n
    `is_admin`: Определяет, является ли пользователь админом\n
    `is_employee`: Определяет, является ли пользователь сотрудником
    """

    try:
        user = User(user_id=user_id, tag=tag, is_admin=is_admin, is_employee=is_employee,
                    created_at=datetime.now(), updated_at=datetime.now())
        await user.create()
    except UniqueViolationError:
        pass


async def select_all() -> list:
    """
    Возвращает список со всеми пользователями
    """

    all_users = await User.query.gino.all()
    return all_users


async def select_all_admins() -> list:
    """
    Возвращает список со всеми админами
    """

    all_admins = await User.query.where(User.is_admin == True).gino.all()
    return all_admins


async def select_all_employes() -> list:
    """
    Возвращает список со всеми сотрудниками
    """

    all_employees = await User.query.where(User.is_employee == True).gino.all()
    return all_employees


async def select_by_tag(tag: str) -> User:
    """
    Возвращает пользователя, которого находит по аргументу tag

    `tag`: Тэг пользователя в Telegram
    """

    user = await User.query.where(User.tag == tag).gino.first()
    return user


async def select(user_id: int) -> User:
    """
    Возвращает пользователя, которого находит по аргументу user_id

    `user_id`: ID пользователя в Telegram
    """

    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update(id: int, user_id: int, tag: str, is_admin: bool, is_employee: bool) -> None:
    """
    Функция для обновления записи о пользователе в бд

    `id`: ID пользователя в БД\n
    `user_id`: ID пользователя в Telegram\n
    `tag`: Тэг пользователя в Telegram\n
    `is_admin`: Определяет, является ли пользователь админом\n
    `is_employee`: Определяет, является ли пользователь сотрудником
    """

    user = await User.get(id)
    if user_id is not None:
        await user.update(user_id=user_id, updated_at=datetime.now()).apply()
    if tag is not None:
        await user.update(tag=tag, updated_at=datetime.now()).apply()
    if is_admin is not None:
        await user.update(is_admin=is_admin, updated_at=datetime.now()).apply()
    if is_employee is not None:
        await user.update(is_employee=is_employee, updated_at=datetime.now()).apply()


async def delete(user_id: int) -> None:
    """
    Функция удаления пользователя из бд

    `user_id`: ID пользователя в Telegram
    """
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.delete()
