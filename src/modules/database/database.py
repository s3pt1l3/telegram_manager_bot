from gino import Gino
from gino.schema import GinoSchemaVisitor
import sqlalchemy as sa
from typing import List
from aiogram import Dispatcher

from modules.config.db_config import POSTGRES_URI

db = Gino()


async def create_db():
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    # Создаем таблицы
    # await db.gino.drop_all()
    # await db.gino.create_all()


class BaseModel(db.Model):
    """
    Класс базовой таблицы
    """

    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(
            f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


async def on_startup(dispatcher: Dispatcher):
    print('Установка связи с PostgreSQL...')
    await db.set_bind(POSTGRES_URI)
