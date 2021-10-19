from sqlalchemy import sql, Column, BigInteger, Text, Date, DateTime, ForeignKey
from asyncpg import UniqueViolationError
from datetime import datetime, date

from modules.database import database as db


class CalendarTask(db.BaseModel):
    """
    Класс модели таблицы задач для сотрудников
    """

    __tablename__ = 'CalendarTasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(
        'Users.user_id', ondelete="CASCADE"))
    task_text = Column(Text)
    task_date = Column(Date)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, task_text: str, task_date: DateTime):
    """
    Функция для добавления задачи в бд

    `user_id`: ID пользователя в Telegram\n
    `task_text`: Задача для сотрудника\n
    `task_date`: Дата задачи
    """

    try:
        task = CalendarTask(user_id=user_id, task_text=task_text, task_date=task_date,
                            created_at=datetime.now(), updated_at=datetime.now())
        await task.create()
    except UniqueViolationError:
        pass


async def select_all() -> list:
    """
    Возвращает список со всеми задачами
    """

    all_tasks = await CalendarTask.query.gino.all()
    return all_tasks


async def select(task_id: int) -> CalendarTask:
    """
    Возвращает задачу, которую находит по аргументу task_id

    `task_id`: ID задачи
    """

    task = await CalendarTask.query.where(CalendarTask.task_id == task_id).gino.first()
    return task

async def select_by_user(user_id: int) -> list:
    """
    Возвращает все еженедельные задачи, которые находит по аргументу user_id

    `user_id`: ID еженедельной задачи
    """
    tasks = await CalendarTask.query.where(CalendarTask.user_id == user_id).gino.all()
    return tasks

async def select_by_user_and_day(user_id: int, day: date) -> list:
    """
    Возвращает список с задачами, которые находит по аргументам user_id и day

    `user_id`: ID пользователя в Telegram
    `day`: Дата задачи
    """

    tasks = await CalendarTask.query.where((CalendarTask.user_id == user_id) & (CalendarTask.task_date == day)).gino.all()
    return tasks


async def update(task_id: int, user_id: int, task_text: str, task_date: DateTime) -> None:
    """
    Функция для обновления записи о задаче в бд

    `task_id`: ID задачи\n
    `user_id`: ID пользователя в Telegram\n
    `task_text`: Текст задачи\n
    `task_date`: Дата задачи
    """

    task = await CalendarTask.get(task_id)
    if user_id is not None:
        await task.update(user_id=user_id, updated_at=datetime.now()).apply()
    if task_text is not None:
        await task.update(task_text=task_text, updated_at=datetime.now()).apply()
    if task_date is not None:
        await task.update(task_date=task_date, updated_at=datetime.now()).apply()


async def delete(task_id: int) -> None:
    """
    Функция удаления задачи из бд

    `task_id`: ID задачи
    """

    task = await CalendarTask.query.where(CalendarTask.task_id == task_id).gino.first()
    await task.delete()
