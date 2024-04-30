from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
import asyncio
import logging
from Py_files.config import BOT_TOKEN
from Py_files.messages import Message
from Py_files import markups as nav
from Py_files.yndx_dict import get_info_about_word
from Py_files.database import db

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()
# Экземпляр класса для работы с сообщениями
ms = Message(bot)


# Обработчик команды /start
@dp.message(Command('start'))
async def start(message: types.Message):
    await ms.output_text(
        message.from_user.id,
        f'Здравствуйте, <b>{message.from_user.first_name}</b>!\n\nВыберите язык, с которым будет идти дальнейшая работа:'
        f'\n\nЕго всегда можно изменить командой /change_language',
        menu=nav.language_menu
    )
    if not db.person_exists(message.from_user.id):
        db.set_person(message.from_user.id)


# Обработчик команды /change_language
@dp.message(Command('change_language'))
async def change_language(message: types.Message):
    await ms.output_text(
        message.from_user.id,
        'Выберите язык, с которым будет идти дальнейшая работа:',
        menu=nav.language_menu
    )


# Обработка кнопки Русский
@dp.callback_query(F.data == 'btn_ru')
async def btn_rus(rus: types.CallbackQuery):
    await ms.delete_and_output_text(
        rus.from_user.id,
        rus.message.message_id,
        '<b>Отлично!</b>\n\nТеперь вы можете написать боту слово на русском языке, и он выдаст его синонимы'
    )
    db.set_language(
        rus.from_user.id,
        language='rus'
    )


# Обработка кнопки English
@dp.callback_query(F.data == 'btn_en')
async def btn_eng(eng: types.CallbackQuery):
    await ms.delete_and_output_text(
        eng.from_user.id,
        eng.message.message_id,
        '<b>Отлично!</b>\n\nТеперь вы можете написать боту слово на английском языке, и он выдаст его синонимы'
    )
    db.set_language(
        eng.from_user.id,
        language='eng'
    )


# Обработчик входящих сообщений
@dp.message(F.text)
async def main(message: types.Message):
    await ms.output_text(message.from_user.id, get_info_about_word(message.from_user.id, message.text))


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
