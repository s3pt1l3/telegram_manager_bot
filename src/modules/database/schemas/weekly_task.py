from sqlalchemy import sql, Column, BigInteger, Text, DateTime, ForeignKey
from asyncpg import UniqueViolationError
from datetime import datetime

from modules.database import database as db


class WeeklyTask(db.BaseModel):
    """
    Класс модели таблицы еженедельных задач для сотрудников
    """

    __tablename__ = 'WeeklyTasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id', ondelete="CASCADE"))
    task_text = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, task_text: str):
    """
    Функция для добавления задачи в бд

    `user_id`: ID пользователя в Telegram\n
    `task_text`: Еженедельная задача для сотрудника
    """

    try:
        user = WeeklyTask(user_id=user_id, task_text=task_text, created_at=datetime.now(), updated_at=datetime.now())
        await user.create()
    except UniqueViolationError:
        pass


async def select_all() -> list:
    """
    Возвращает список со всеми еженедельными задачами
    """

    all_tasks = await WeeklyTask.query.gino.all()
    return all_tasks


async def select(task_id: int) -> WeeklyTask:
    """
    Возвращает еженедельную задачу, которую находит по аргументу task_id

    `task_id`: ID ежедневной задачи
    """

    task = await WeeklyTask.query.where(WeeklyTask.task_id == task_id).gino.first()
    return task

async def select_by_user(user_id: int) -> WeeklyTask:
    """
    Возвращает все еженедельные задачи, которые находит по аргументу user_id

    `user_id`: ID еженедельной задачи
    """

    tasks = await WeeklyTask.query.where(WeeklyTask.user_id == user_id).gino.all()
    return tasks


async def update(task_id: int, user_id: int, task_text: str) -> None:
    """
    Функция для обновления записи о еженедельной задаче в бд

    `task_id`: ID еженедельной задачи\n
    `user_id`: ID пользователя в Telegram\n
    `task_text`: Текст еженедельной задачи
    """

    task = await WeeklyTask.get(task_id)
    if user_id is not None:
        await task.update(user_id=user_id, updated_at=datetime.now()).apply()
    if task_text is not None:
        await task.update(task_text=task_text, updated_at=datetime.now()).apply()


async def delete(task_id: int) -> None:
    """
    Функция удаления еженедельной задачи из бд

    `task_id`: ID еженедельной задачи
    """

    task = await WeeklyTask.query.where(WeeklyTask.task_id == task_id).gino.first()
    await task.delete()
