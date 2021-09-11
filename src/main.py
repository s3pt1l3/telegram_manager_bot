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


def bind_filters(dp, *args):
    """
    `args`: фильтры
    `dp`: Dispatcher
    """
    for fltr in args:
        dp.bind_filter(fltr)


if __name__ == '__main__':
    from aiogram import executor
    from apps import dp
    from apps import _filters

    bind_filters(dp, _filters)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
