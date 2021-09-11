from sqlalchemy import sql, Column, BigInteger, Text, DateTime
from config.db_config import database as db

class Task(db.BaseModel):
    """
    Класс модели таблицы задач для сотрудников
    """

    __tablename__ = 'Tasks'

    user_id = Column(BigInteger, db.ForeignKey('Users.user_id'), primary_key=True)
    task_text = Column(Text)
    task_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    query: sql.Select
    