from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



ID = None


#загрузка нового товара фото, имя, описание, цена, количетво
class FSMcategory(StatesGroup):
    category_name = State()
    category_id = State()

class FSMAdmin(StatesGroup):
    photo = State()
    product_id = State()
    name = State()
    description = State()
    price = State()
    quantity = State()
    category_id_1 = State()
    


#
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что нужно хозяин?', reply_markup=admin_kb.button_case_admin)
    await message.delete()



async def add_category(message : types.Message):
    if message.from_user.id == ID:
        await FSMcategory.category_name.set()
        await message.reply('Имя категории')

async def category_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as dat:
            dat['category_name'] = message.text
            await FSMcategory.next()
            await message.reply('Номер категории')
   
async def category_id(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as dat:
            dat['category_id'] = int(message.text)

        await sqlite_db.sql_add_command_2(state)
        await state.finish()
        await message.reply('ok')



#загрузка фото
#@dp.message_handler(commands='Загрузить', State=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузить фото')

#команда отмены загрузки товара
#@dp.message_handler(state='*', commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return      
        await state.finish()
        await message.reply('OK')


#загрузка фото
#@dp.message_handler(content_types=['photo'], state=FSMAdmin)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply('Задайте id номер товара')


async def product_id(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['product_id'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Теперь введите название')
#название
#@dp.message_handler(State=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
            await FSMAdmin.next()
            await message.reply('Введите описание')

#описание
#@dp.message_handler(State=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
            await FSMAdmin.next()
            await message.reply('Укажите цену в рублях')


#цена
#@dp.message_handler(State=FSMAdmin.price)
async def load_price(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
            await FSMAdmin.next()
            await message.reply('Укажите количество')


#количество
#@dp.message_handler(State=FSMAdmin.quantity)
async def load_quantity(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['quantity'] = int(message.text)
            await FSMAdmin.next()
            await message.reply('Укажите категорию')
        

async def load_category_id(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['category_id_1'] = int(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('ok')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)

#удаление товаров
@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-2]}руб.\nКоличество {ret[-1]}')
            await bot.send_message(message.from_user.id, text='Хотите удалить товар?', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


#статистика посещения бота        
#@dp.message_handler(commands='статистика')
#async def statistics(message: types.Message):
    
        


#покупки покупателей 
@dp.message_handler(commands='покупки')
async def purchases(message: types.Message):
    if message.from_user.id == ID:
            await bot.send_message(message.from_user.id, 'ке',reply_markup=admin_kb.button_case_admin)


#
def register_handlers_admin(dp : dispatcher): 
    dp.register_message_handler(add_category, commands=['Добавить_категорию'], state=None)
    dp.register_message_handler(category_name,state=FSMcategory.category_name)
    dp.register_message_handler(category_id, state=FSMcategory.category_id)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command,commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(product_id, state=FSMAdmin.product_id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_quantity, state=FSMAdmin.quantity)
    dp.register_message_handler(load_category_id, state=FSMAdmin.category_id_1)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    #dp.register_message_handler(statistics, commands='статистика')
    dp.register_message_handler(purchases, commands='покупки')
    

