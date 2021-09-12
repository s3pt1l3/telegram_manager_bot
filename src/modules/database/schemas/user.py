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
    user_id = Column(BigInteger)
    tag = Column(String, 100)
    is_admin = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, tag: str, is_admin: bool):
    """
    Функция для добавления пользователя в бд

    `user_id`: ID пользователя в Telegram\n
    `tag`: Тэг пользователя в Telegram\n
    `is_admin`: Определяет, является ли пользователь админом
    """

    try:
        user = User(user_id=user_id, tag=tag, is_admin=is_admin, created_at=datetime.now(), updated_at=datetime.now()) 
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

    all_admins = await User.query.where(User.is_admin).gino.all()
    return all_admins


async def select_all_employes() -> list:
    """
    Возвращает список со всеми сотрудниками
    """

    all_employes = await User.query.where(User.is_admin).gino.all()
    return all_employes


async def select_by_tag(tag: str) -> User:
    """
    Возвращает пользователя, которого нахдит по аргументу tag

    `tag`: Тэг пользователя в Telegram
    """

    user = await User.query.where(User.tag == tag).gino.first()
    return user


async def select(user_id: int) -> User:
    """
    Возвращает пользователя, которого нахдит по аргументу user_id

    `user_id`: ID пользователя в Telegram
    """

    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update(user_id: int, tag: str, is_admin: bool) -> None:
    """
    Функция для обновления записи о пользователе в бд

    `user_id`: ID пользователя в Telegram\n
    `tag`: Тэг пользователя в Telegram\n
    `is_admin`: Определяет, является ли пользователь админом
    """

    user = await User.get(user_id)
    if user_id is not None:
        await user.update(user_id=user_id, updated_at=datetime.now()).apply()
    if tag is not None:
        await user.update(tag=tag, updated_at=datetime.now()).apply()
    if is_admin is not None:
        await user.update(is_admin=is_admin, updated_at=datetime.now()).apply()


async def delete(user_id: int) -> None:
    """
    Функция удаления пользователя из бд

    `user_id`: ID пользователя в Telegram
    """
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.delete()
