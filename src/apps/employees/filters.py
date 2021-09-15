from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from modules.database.schemas import user


class IsEmployee(BoundFilter):
    """Проверяет, сотрудник ли отправил сообщение"""
    key = 'is_employee'

    async def check(self, message: types.Message):
        employees = [user.user_id for user in await user.select_all_employes()]
        return message.from_user.id in employees
