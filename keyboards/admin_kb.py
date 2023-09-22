from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


#
button_category = KeyboardButton('/Добавить_категорию')
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_purchases=KeyboardButton('/Покупки')
button_statistics=KeyboardButton('/Статистика')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load,button_category,button_delete).add(button_purchases,button_statistics)