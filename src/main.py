from loader import dp


async def on_startup(dp):
    pass

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
