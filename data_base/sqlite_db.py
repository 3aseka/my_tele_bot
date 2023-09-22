import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#база данных товара
def sql_start():
    global base, cur 
    base = sq.connect('vkr_magazine.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY, img TEXT,product_id INT, name TEXT, description TEXT, price INT, count INT,category_id INT)')
    base.execute('CREATE TABLE IF NOT EXISTS categories(category_name TEXT,category_id INT)')
    base.execute('CREATE TABLE IF NOT EXISTS basket(id INTEGER PRIMARY KEY,user_id INT, product_id INT,count INT)')
    base.execute('CREATE TABLE IF NOT EXISTS statistics(id TEXT PRIMARY KEY, name TEXT, quantity INT, price INT)')
    base.commit()

#Добавление товара
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu(img,product_id,name,description,price,count,category_id) VALUES (?,?,?,?,?,?,?)', tuple(data.values()))
        base.commit()

#Добавление категории
async def sql_add_command_2(state):
    async with state.proxy() as dat:
        cur.execute('INSERT INTO categories VALUES (?,?)', tuple(dat.values()))
        base.commit()
#Меню товаров
#async def sql_read(message):
    #for ret in cur.execute('SELECT * FROM menu').fetchall():
       # await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-2]}руб.\nКоличество {ret[-1]}')
        #await bot.send_message(message.from_user.id, text='Желаете добавить товар в корзину?', reply_markup=InlineKeyboardMarkup()\
           # .add(InlineKeyboardButton('Добавить в корзину', callback_data='Добавлено')))

#удаление товара
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data): 
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

