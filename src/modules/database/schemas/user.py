from sqlalchemy import sql, Column, BigInteger, Boolean, String, DateTime
from config.db_config import database as db
from asyncpg import UniqueViolationError


class User(db.BaseModel):
    """
    Класс модели таблицы пользователей бота
    """

    __tablename__ = 'Users'

    user_id = Column(BigInteger, primary_key=True)
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
        user = User(user_id=user_id, tag=tag, is_admin=is_admin)
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
    if tag is not None:
        await user.update(tag=tag).apply()
    if is_admin is not None:
        await user.update(is_admin=is_admin).apply()


async def delete(user_id: int) -> None:
    """
    Функция удаления пользователя из бд

    `user_id`: ID пользователя в Telegram
    """
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.delete()
