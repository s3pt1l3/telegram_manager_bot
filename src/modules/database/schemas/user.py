from sqlalchemy import sql, Column, BigInteger, Boolean, String, DateTime
from config.db_config import database as db

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
    