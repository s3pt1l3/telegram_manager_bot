from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import dp
from ..filters import IsAdmin
from modules.database.schemas import user
from modules.database.schemas import (calendar_task, daily_task,
                                      perpetual_task, weekly_task)


@dp.message_handler(IsAdmin(), commands=['delete_task'], state='*')
async def delete_task(message: Message, state: FSMContext):
    args = message.get_args()
    if not args:
        await message.answer('Использование: /delete_task [ID]')
        return
    _id = args[0]
    if _id.startswith('c'):
        await calendar_task.delete(int(_id[1:]))
    if _id.startswith('d'):
        await daily_task.delete(int(_id[1:]))
    if _id.startswith('p'):
        await perpetual_task.delete(int(_id[1:]))
    if _id.startswith('w'):
        await weekly_task.delete(int(_id[1:]))
    await message.answer('Удалено')
