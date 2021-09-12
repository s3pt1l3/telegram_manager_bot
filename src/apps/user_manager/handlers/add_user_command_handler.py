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
    await user.update(usr.user_id, args[0], usr.is_admin)
