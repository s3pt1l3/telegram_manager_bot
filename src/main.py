from loader import dp

async def flush_all():
    from loader import db
    
    print('Очистка базы...')
    await db.gino.drop_all()
    print('Готово')
    print('Создание таблиц...')
    await db.gino.create_all()
    print('Готово')

async def on_startup(dp):
    from modules.database import database
    
    print('Подключение к базе данных...')
    await database.on_startup(dp)
    print('Подключение установлено')
    await flush_all()

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
