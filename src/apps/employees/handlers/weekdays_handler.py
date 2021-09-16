from datetime import date, datetime
from aiogram.types import Message, CallbackQuery, callback_query, message
from aiogram.dispatcher import FSMContext
from loader import dp
from ..filters import IsEmployee
from ..keyboards.inline import get_weekdays_keyboard
from modules.database.schemas import daily_task, calendar_task


@dp.message_handler(IsEmployee(), commands=['tasks'], state='*')
async def weekdays(message: Message, state: FSMContext):
    await message.answer('Выберите день', reply_markup=get_weekdays_keyboard())


@dp.callback_query_handler(IsEmployee(), text_contains='weekday', state='*')
async def weekdays(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    day = date(int(call.data[8:].split(
        '-')[0]), int(call.data[8:].split('-')[1]), int(call.data[8:].split('-')[2]))
    calendar_tasks = await calendar_task.select_by_user_and_day(user_id, day)
    daily_tasks = await daily_task.select_by_user(user_id)
    count = 1

    mes = 'Ваши задачи на этот день:'
    for task in calendar_tasks:
        mes += f'\n{count}. {task.task_text}'
        count += 1

    mes += '\n\nЕжедневные задачи:'
    count = 1
    for task in daily_tasks:
        mes += f'\n{count}. {task.task_text}'
        count += 1

    await call.message.answer(mes)
