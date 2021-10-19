from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import dp
from modules.database.schemas import (calendar_task, daily_task,
                                      perpetual_task, user, weekly_task)

from ..filters import IsAdmin


@dp.message_handler(IsAdmin(), commands=['tasks'], state='*')
async def task_history(message: Message, state: FSMContext):
    msg = ""
    calendar_t = await calendar_task.select_all()
    daily_t = await daily_task.select_all()
    perpetual_t = await perpetual_task.select_all()
    weekly_t = await weekly_task.select_all()

    for task in calendar_t:
        msg += f"id: c{task.task_id}\n{task.task_text}\n{task.task_date}\n@{(await user.select(task.user_id)).tag}"
        await message.answer("Календарные задачи\n" + msg)
        msg = ""

    for task in daily_t:
        msg += f"id: d{task.task_id}\n{task.task_text}\n@{(await user.select(task.user_id)).tag}"
        await message.answer("Ежедневные задачи\n" + msg)
        msg = ""
    for task in perpetual_t:
        msg += f"id: p{task.task_id}\n{task.task_text}\n@{(await user.select(task.user_id)).tag}"
        await message.answer("Бессрочные задачи\n" + msg)
        msg = ""
    for task in weekly_t:
        msg += f"id: w{task.task_id}\n{task.task_text}\n@{(await user.select(task.user_id)).tag}"
        await message.answer("Еженедельные задачи\n" + msg)
        msg = ""
