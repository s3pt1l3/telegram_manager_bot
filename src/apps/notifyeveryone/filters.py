from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from modules.database.schemas import user


class IsAdmin(BoundFilter):
    """Проевряет админ ли отправил сообщение"""
    key = 'is_admin'

    async def check(self, message: types.Message):
        admins = [user.user_id for user in await user.select_all_admins()]
        return message.from_user.id in admins
