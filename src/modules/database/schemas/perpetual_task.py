from sqlalchemy import sql, Column, BigInteger, Text, DateTime, ForeignKey
from asyncpg import UniqueViolationError
from datetime import datetime

from modules.database import database as db


class PerpetualTask(db.BaseModel):
    """
    Класс модели таблицы бессрочных задач для сотрудников
    """

    __tablename__ = 'PerpetualTasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id', ondelete="CASCADE"))
    task_text = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select


async def add(user_id: int, task_text: str):
    """
    Функция для добавления бессрочной задачи в бд

    `user_id`: ID пользователя в Telegram\n
    `task_text`: Бессрочная задача для сотрудника
    """

    try:
        user = PerpetualTask(user_id=user_id, task_text=task_text, created_at=datetime.now(), updated_at=datetime.now())
        await user.create()
    except UniqueViolationError:
        pass


async def select_all() -> list:
    """
    Возвращает список со всеми бессрочными задачами
    """

    all_tasks = await PerpetualTask.query.gino.all()
    return all_tasks


async def select(task_id: int) -> PerpetualTask:
    """
    Возвращает бессрочную задачу, которую нахдит по аргументу task_id

    `task_id`: ID бессрочной задачи
    """

    task = await PerpetualTask.query.where(PerpetualTask.task_id == task_id).gino.first()
    return task


async def update(task_id: int, user_id: int, task_text: str) -> None:
    """
    Функция для обновления записи о бессрочной задаче в бд

    `task_id`: ID бессрочной задачи\n
    `user_id`: ID пользователя в Telegram\n
    `task_text`: Текст бессрочной задачи
    """

    task = await PerpetualTask.get(task_id)
    if user_id is not None:
        await task.update(user_id=user_id, updated_at=datetime.now()).apply()
    if task_text is not None:
        await task.update(task_text=task_text, updated_at=datetime.now()).apply()


async def delete(task_id: int) -> None:
    """
    Функция удаления бессрочной задачи из бд

    `task_id`: ID бессрочной задачи
    """

    task = await PerpetualTask.query.where(PerpetualTask.user_id == task_id).gino.first()
    await task.delete()
