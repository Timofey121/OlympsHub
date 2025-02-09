# -*- coding: utf8 -*-
import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, add_user, count_users


@dp.message_handler(Command("start"))
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Бот создан для помощи ученикам, которые хотят поступить в ВУЗ по олимпиадам. \n"
                         f"Бот предоставит информацию об олимпиадах по нужным предметам и напомнит Вам о них "
                         f"(за 1 день).", reply_markup=main_keyboard)
    try:
        if len(list(await subscriber_exists(telegram_id=str(message.from_user.id)))) == 0:
            data_registration = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'),
                                                           '%Y%m%d').date()
            await add_user(telegram_id=str(message.from_user.id), full_name=message.from_user.full_name,
                           blocked=0, data_registration=data_registration)
            for admin in ADMINS:
                try:
                    await dp.bot.send_message(admin,
                                              f"Сообщение для админов:\n"
                                              f"+1 Пользователь!\n\n"
                                              f"В бот зашел(а):\n"
                                              f"Full_name = {message.from_user.full_name}\n"
                                              f"is_bot = {'Не бот!' if message.from_user.is_bot is False else 'Бот!'}\n"
                                              f"User_name = @{'Нет значения' if message.from_user.username is None else message.from_user.username}\n"
                                              f"ID = {message.from_user.id}\n"
                                              f"Language = {message.from_user.language_code}\n\n"
                                              f"Всего пользователей ==> {list(await count_users())[0][0]}")
                except Exception as ex:
                    print(ex)
    except Exception as ex:
        print(ex)
