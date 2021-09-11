async def on_startup(dp):
    from apps import _filters
    from loader import dp

    dp.bind_filter(*_filters)

if __name__ == '__main__':
    from aiogram import executor
    from apps import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
