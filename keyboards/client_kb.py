from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Адрес')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Корзина')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1,b2,b3).add(b4)