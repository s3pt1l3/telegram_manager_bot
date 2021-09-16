import asyncio
from modules.scheduler.tasks_scheduler import scheduler
from modules.database.schemas import user


async def flush_all():
    from loader import db

    print('Очистка базы...')
    await db.gino.drop_all()
    print('Готово')
    print('Создание таблиц...')
    await db.gino.create_all()
    print('Готово')


async def on_startup(dp):
    from loader import dp
    from modules.database import database

    print('Подключение к базе данных...')
    await database.on_startup(dp)
    print('Подключение установлено')
    await flush_all()

    await user.add(552314671, 's3pt1l3', True, False)
    await user.add(626041522, 'xcanary', True, False)
    await user.add(235995491, 'sodamea', True, False)

    asyncio.create_task(scheduler())


def bind_filters(dp, *args):
    """
    `args`: фильтры
    `dp`: Dispatcher
    """
    filters = args[0]
    for fltr in filters:
        dp.bind_filter(fltr)


if __name__ == '__main__':
    from aiogram import executor
    from apps import dp
    from apps import _filters

    bind_filters(dp, _filters)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
