from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db

#изменение показаний в файле запуска bat 
async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


from handlers import clients, admin, other    

clients.register_handlers_clients(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)