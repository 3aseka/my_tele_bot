from aiogram import types, dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,PreCheckoutQuery,CallbackQuery,LabeledPrice,Message
from aiogram.dispatcher.filters import Command
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from services import DataBase
from config import Config

cb = CallbackData('btn', 'type', 'product_id', 'category_id')
db = DataBase('vkr_magazine.db')

#class FSMClient(StatesGroup):
    #id = State()
    #name = State()

#реакция на /start /help
#@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    try:
        name = message.from_user.username

        await bot.send_message(message.from_user.id, f"Привет, {name}!\nТы попал в бота магазин!\nТы можешь использовать кнопки или команды '/'.", reply_markup=kb_client)
        await message.delete()
        
        #await bot.send_message(message.from_user.id, 'Привет', reply_markup=kb_client)
        #await message.delete()
        #await statistics_db.sql_add_commands(state)
        #await basket_db.sql_add_commands(state)
        #await state.finish()
    except:
        await message.reply('ошибка')

#@dp.message_handler(commands=['help'])       
async def command_help(message : types.Message):
    await bot.send_message(message.from_user.id, 'help')

#показывает время работы
#@dp.message_handler(commands=['Режим_работы'])
async def open_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 20:00, Сб-Вс с 10:00 до 18:00')


#показывает адрес
#@dp.message_handler(commands=['Адрес'])
async def location_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'г.Такой-то ул. Такаята номер')

#клавиатура добавления товара
async def gen_menu(data, user_id):
    keyboard = InlineKeyboardMarkup()
    for i in data:
        count = await db.get_count_in_basket(user_id, i[2])
        count = 0 if not count else sum(j[0] for j in count)
        keyboard.add(InlineKeyboardButton(text=f':{i[3]}: {i[5]}p - {count}шт. ,\n {i[4]}',callback_data=f'btn:plus:{i[2]}:{i[7]}'))
        keyboard.add(InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[2]}:{i[7]}'),
                     InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[2]}:{i[7]}'),
                     InlineKeyboardButton(text='❌', callback_data=f'btn:del:{i[2]}:{i[7]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:-:-'))

    return keyboard

@dp.message_handler(commands=('Меню'))
async def vkr_menu_command(message : types.Message):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))

    await message.answer('Что хотите купить?', reply_markup=keyboard)
 

@dp.callback_query_handler(cb.filter(type='category'))
async def goods(call: CallbackQuery, callback_data: dict):
    data = await db.get_menu(callback_data.get('category_id'))
    keyboard = await gen_menu(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='back'))
async def back(call: CallbackQuery):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='minus'))
async def minus(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await db.get_count_in_basket(call.message.chat.id, product_id)
    if not count_in_cart or count_in_cart[0][0] == 0:
        await call.message.answer('Товар в  корзине отсутсвует!')
        return 0
    elif count_in_cart[0][0] == 1:
        await db.remove_one_item(product_id, call.message.chat.id)
    else:
        await db.change_count(count_in_cart[0][0] - 1, product_id, call.message.chat.id)

    data = await db.get_menu(callback_data.get('category_id'))
    keyboard = await gen_menu(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='plus'))
async def plus(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await db.get_count_in_basket(call.message.chat.id, product_id)
    count_in_stock = await db.get_count_in_menu(product_id)
    if count_in_stock[0][0] == 0:
        await call.message.answer('Товара нет в наличии :(')
        return 0
    elif not count_in_cart or count_in_cart[0][0] == 0:
        await db.add_to_basket(call.message.chat.id, product_id)
        await call.message.answer('Добавил!')
    elif count_in_cart[0][0] < count_in_stock[0][0]:
        await db.change_count(count_in_cart[0][0] + 1, product_id, call.message.chat.id)
    else:
        await call.message.answer('Больше нет в наличии')
        return 0
        
    data = await db.get_menu(callback_data.get('category_id'))
    keyboard = await gen_menu(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='del'))
async def delete(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart = await db.get_count_in_basket(call.message.chat.id, product_id)
    if not count_in_cart:
        await call.message.answer('Товар в корзине отсутствует!')
        return 0
    else:
        await db.remove_one_item(product_id, call.message.chat.id)

    data = await db.get_menu(callback_data.get('category_id'))
    keyboard = await gen_menu(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)


@dp.message_handler(commands=['Корзина'])
async def vkr_basket_command(message : types.Message):
    data = await db.empty_basket(message.chat.id)
    for i in data:
            await bot.send_message(message.chat.id, text=f'{i[2]},{i[3]}')

    #await message.answer("пусто")
    



   
@dp.message_handler(Command('pay'))
async def buy(message: Message):
    data = await db.get_basket(message.chat.id)
    new_data = []
    for i in range(len(data)):
        new_data.append(await db.get_user_menu(data[i][2]))
    new_data = [new_data[i][0] for i in range(len(new_data))]
    prices = [LabeledPrice(label=new_data[i][3]+f' x {data[i][2]}',amount=new_data[i][5]*100*data[i][3]) for i in range(len(new_data))]
    await bot.send_invoice(message.chat.id,
                           title='Cart',
                           description='Description',
                           provider_token=Config.pay_token,
                           currency='rub',
                           need_email=True,
                           prices=prices,
                           start_parameter='example',
                           payload='some_invoice')

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def s_pay(message: Message):
    await db.empty_basket(message.chat.id)
    await bot.send_message(message.chat.id, 'Платеж прошел успешно!!!')



def register_handlers_clients(dp : dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(open_command, commands=['Режим_работы'])
    dp.register_message_handler(location_command, commands=['Адрес'])
    dp.register_message_handler(vkr_menu_command, commands=['Меню'])
    dp.register_message_handler(vkr_basket_command, commands=['Корзина'])