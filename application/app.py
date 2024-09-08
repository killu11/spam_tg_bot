import asyncio
import logging
import sys
import os

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from database import Database
from aiogram import types
from keyboards import Buttons
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import Message
from time import sleep


dotenv_path = os.path.join(os.path.dirname('bot_maksim'), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


API_KEY = os.environ["API_KEY"]
if not API_KEY :
    raise ValueError('Либо апи ключ стух, либо ты дубина его нормально не ввел в переменное окружение')

"""""
bot - объект, делающий рассылку 

Dispatcher - объект, запускающий бота, передающий событие в обработчик событий с соотвествующей функцией.
"""""

bot = Bot(token = API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) :

    db = Database()
    user_id = message.from_user.id
    if db.get_current_admin(user_id): ##является ли юзер, обращающийся к боту АДМИНОМ
        admin_keyboard = types.InlineKeyboardMarkup(inline_keyboard = [[Buttons.reboot_spam.value]]) ##панель для админа
        
        await message.answer(text = f'Доброго времени суток, {message.from_user.full_name}!\n{html.bold('Выберите один из пунктов меню:')}', reply_markup = admin_keyboard)
        db.connect.close()

    else : 
        user_keyboard = types.InlineKeyboardMarkup(inline_keyboard= [[Buttons.info_about_creators.value]])##панелька для работяги

        await message.answer(f'Здравствуйте,{message.from_user.full_name}, чем могу помочь?', reply_markup=user_keyboard)
        db.connect.close

@dp.callback_query()
async def get_contacts(callback_query: types.CallbackQuery):
    if callback_query.data == 'contact':
        await bot.send_message(chat_id = callback_query.from_user.id , text = 'По всем вопросам обращаться к 👉 <a href = "https://t.me/Shinshilladmin">Администратору</a>.')

@dp.callback_query()
async def start_spam_button(callback_query: types.CallbackQuery):
    try:
        db = Database()
        groups_id = db.read_groups()
        data_array = [item[0] for item in groups_id]
        db.connect.close()
        
        if callback_query.data == 'reboot_spam':
            await bot.send_message(chat_id = callback_query.from_user.id, text = 'Рассылка возобновлена')
            while True:
                for id in data_array:
                    await bot.send_message(chat_id= id, text ='🎮 Создание аккаунта для покупки игр на PS4, PS5\n\n\
💸 Подписки для PlayStation, пополнение счета, покупка игр\n\n\
🤓 Свежие новости игровой индустрии, акции, конкурсы\n\n\
😎 Переходи и подписывайся 👉 <a href = "https://t.me/ShinshillaPay">Shinshilla Pay</a>', parse_mode=ParseMode.HTML)
                    await asyncio.sleep(30)

    except TelegramForbiddenError:
            db = Database()
            db.delete_group(id)
            await bot.send_message(chat_id = '869803539', text = f'Был удален из бд следущий чат: {id}')
        

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed = JOIN_TRANSITION))
async def add_to_chat(chat_member_updated: types.ChatMemberUpdated) :

    CMU = chat_member_updated
   
    if CMU.new_chat_member.status == 'member' and CMU.old_chat_member.status == 'left':
        try:
            db = Database()
            db.create_new_group(CMU.chat.id)
        except Exception as e:
            print(e)

        while True:
                await bot.send_message(chat_id= CMU.chat.id , text ='🎮 Создание аккаунта для покупки игр на PS4, PS5\n\n\
💸 Подписки для PlayStation, пополнение счета, покупка игр\n\n\
🤓 Свежие новости игровой индустрии, акции, конкурсы\n\n\
😎 Переходи и подписывайся 👉 <a href = "https://t.me/ShinshillaPay">Shinshilla Pay</a>', parse_mode=ParseMode.HTML)
                await asyncio.sleep(30)


async def main() :
    await dp.start_polling(bot) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
