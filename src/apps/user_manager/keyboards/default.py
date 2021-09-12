from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_all_employes_keyboard(employes: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    for emp in employes:
        keyboard.add(KeyboardButton(str(emp.tag)))
    return keyboard
