from aiogram import types, dispatcher
from create_bot import dp

#@dp.message_handler()
async def echo_send(message : types.message):
    await message.answer(message.text)
    


def register_handlers_other(dp : dispatcher):
    dp.register_message_handler(echo_send)