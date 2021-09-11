from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from modules.database.schemas import user


class IsAdmin(BoundFilter):
    """Проевряет админ ли отправил сообщение"""
    key = 'is_admin'

    async def check(self, message: types.Message):
        admins = await user.select_all_admins()
        return message.from_user.id in admins
