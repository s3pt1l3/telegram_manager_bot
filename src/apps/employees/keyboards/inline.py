from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_weekdays_keyboard() -> InlineKeyboardMarkup:
    year, week = date.today().isocalendar().year, date.today().isocalendar().week
    weekdays_keyboard = InlineKeyboardMarkup(row_width=1)
    weekdays_keyboard.add(InlineKeyboardButton('Понедельник', callback_data=f'weekday:{date.fromisocalendar(year, week, 1)}'),
                          InlineKeyboardButton(
                              'Вторник', callback_data=f'weekday:{date.fromisocalendar(year, week, 2)}'),
                          InlineKeyboardButton(
                              'Среда', callback_data=f'weekday:{date.fromisocalendar(year, week, 3)}'),
                          InlineKeyboardButton(
                              'Четверг', callback_data=f'weekday:{date.fromisocalendar(year, week, 4)}'),
                          InlineKeyboardButton(
                              'Пятница', callback_data=f'weekday:{date.fromisocalendar(year, week, 5)}'),
                          InlineKeyboardButton(
                              'Суббота', callback_data=f'weekday:{date.fromisocalendar(year, week, 6)}'),
                          InlineKeyboardButton('Воскресенье', callback_data=f'weekday:{date.fromisocalendar(year, week, 7)}'))
    return weekdays_keyboard
