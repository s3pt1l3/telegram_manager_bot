from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

task_type_keyboard = InlineKeyboardMarkup(row_width=2)
task_type_keyboard.add(InlineKeyboardButton('Ежедневная', callback_data='task:routine'),
                       InlineKeyboardButton('Без дедлайна', callback_data='task:nodeadline'),
                       InlineKeyboardButton('Календарная', callback_data='task:calendar'))
