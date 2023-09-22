from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

#кнопки ссылки
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Ссылка', url='')
urlButton2 = InlineKeyboardButton(text='Ссылка', url='')
urlkb.add(urlButton,urlButton2)


@dp.message_handler(commands='ссылки')
async def url_command(message : types.Message):
    await message.answer('Ссылочки', reply_markup=urlkb)

inkb= InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='back',callback_data='www'))

@dp.message_handler(commands='test')
async def url_command(message : types.Message):
    await message.answer('Инлайн кнопка', reply_markup=inkb)

@dp.callback_query_handler(text='www')
async def www_call(callback : types.callback_query):
    await callback.message.answer('Нажата инлайн')
    await callback.answer()



executor.start_polling(dp, skip_updates=True)