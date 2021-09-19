from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp
from ..filters import IsAdmin
from modules.database.schemas import user


@dp.message_handler(IsAdmin(), commands=['add'], state='*')
async def handle_add_command(message: Message, state: FSMContext):
    args = message.get_args()

    if not args:
        await message.answer('Использование: /add [Тег пользователя]')
        return

    usr = await user.select_by_tag(args[0])
    if not usr:
        await message.answer('Пользователь не найден')
        return
    await user.update(usr.user_id, args[0], usr.is_admin, True)


@dp.message_handler(IsAdmin(), commands=['addadmin'], state='*')
async def handle_newadmin(message: Message, state: FSMContext):
    args = message.get_args()

    if not args:
        await message.answer('Использование: /addadmin [Тег пользователя]')
        return

    usr = await user.select_by_tag(args[0])
    if not usr:
        await message.answer('Пользователь не найден')
        return
    await user.update(usr.user_id, args[0], True, True)
