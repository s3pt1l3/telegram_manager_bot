from sqlalchemy import sql, Column, BigInteger, Text, DateTime
from asyncpg import UniqueViolationError
from datetime import datetime

from config.db_config import database as db


class Task(db.BaseModel):
    """
    Класс модели таблицы задач для сотрудников
    """

    __tablename__ = 'Tasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, db.ForeignKey('Users.user_id'))
    task_text = Column(Text)
    task_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, task_text: str, task_date: bool):
    """
    Функция для добавления задачи в бд

    `user_id`: ID пользователя в Telegram\n
    `task_text`: Задача для сотрудника\n
    `task_date`: Дата задачи
    """

    try:
        user = Task(user_id=user_id, task_date=task_date, task_date=task_date, created_at=datetime.now(), updated_at=datetime.now())
        await user.create()
    except UniqueViolationError:
        pass


async def select_all() -> list:
    """
    Возвращает список со всеми задачами
    """

    all_tasks = await Task.query.gino.all()
    return all_tasks


async def select(task_id: int) -> Task:
    """
    Возвращает задачу, которую нахдит по аргументу task_id

    `task_id`: ID задачи
    """

    task = await Task.query.where(Task.task_id == task_id).gino.first()
    return task


async def update(task_id: int, user_id: int, tag: str, is_admin: bool) -> None:
    """
    Функция для обновления записи о задаче в бд

    `task_id`: ID задачи\n
    `user_id`: ID пользователя в Telegram\n
    `task_text`: Текст задачи\n
    `task_date`: Дата задачи
    """

    task = await Task.get(task_id)
    if user_id is not None:
        await task.update(user_id=user_id, updated_at=datetime.now()).apply()
    if tag is not None:
        await task.update(tag=tag, updated_at=datetime.now()).apply()
    if is_admin is not None:
        await task.update(is_admin=is_admin, updated_at=datetime.now()).apply()


async def delete(task_id: int) -> None:
    """
    Функция удаления задачи из бд

    `user_id`: ID задачи в Telegram
    """

    task = await Task.query.where(Task.user_id == task_id).gino.first()
    await task.delete()
