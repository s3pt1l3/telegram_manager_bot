from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp
from ..filters import IsAdmin
from modules.database.schemas import user


@dp.message_handler(IsAdmin(), commands=['del'], state='*')
async def handle_del_command(message: Message, state: FSMContext):
    args = message.get_args()

    if not args:
        await message.answer('Использование: /del [Тег пользователя]')
        return

    usr = await user.select_by_tag(''.join(args))
    if not usr:
        await message.answer('Пользователь не найден')
        return
    await user.delete(usr.user_id)
    await message.answer('Пользователь удален')
