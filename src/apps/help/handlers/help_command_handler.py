from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from apps.user_manager.filters import IsAdmin
from loader import dp
from modules.database.schemas import user


@dp.message_handler(commands=['start'])
async def start_command(message: Message, state: FSMContext):
    await user.add(message.from_user.id, message.from_user.username)


@dp.message_handler(IsAdmin(), commands=['help'], state='*')
async def handle_del_command(message: Message, state: FSMContext):
    msg = """
Для добавления сотрудника введите:
    /add [Тег пользователя]

Для добавления админа введите:
    /addadmin [Тег пользователя]

Для удаления пользователя введите:
    /del [Тег пользователя]

Для создания задачи введите:
    /create [Задача]
    """
    await message.answer(msg)


@dp.message_handler(commands=['help'], state='*')
async def handle_del_command(message: Message, state: FSMContext):
    usr = await user.select(message.from_user.id)
    if not usr or not usr.is_employee:
        await message.answer('Нет доступа, свяжитесь с администратором')
        return
    await message.answer('Для просмотра задач введите /tasks')
