# -*- coding: utf8 -*-
import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import ADMINS
from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, add_user, count_users


async def addToBd(message):
    data_registration = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'),
                                                   '%Y%m%d').date()
    await add_user(telegram_id=str(message.from_user.id), full_name=message.from_user.full_name,
                   blocked=0, data_registration=data_registration)
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin,
                                      f"Message for admins:\n"
                                      f"+1 User!\n\n"
                                      f"User entered the bot:\n"
                                      f"Full_name = {message.from_user.full_name}\n"
                                      f"is_bot = {'Not a bot!' if message.from_user.is_bot is False else 'Bot!'}\n"
                                      f"User_name = @{'No value' if message.from_user.username is None else message.from_user.username}\n"
                                      f"ID = {message.from_user.id}\n"
                                      f"Language = {message.from_user.language_code}\n\n"
                                      f"Total users ==> {list(await count_users())[0][0]}")


@dp.message_handler(Command("start"))
async def bot_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!\n"
                         f"This bot was created to help students who want to enter university through olympiads. \n"
                         f"The bot will provide information about olympiads in the subjects you need and remind you about them "
                         f"(1 day before).", reply_markup=main_keyboard)
    try:
        if len(list(await subscriber_exists(telegram_id=str(message.from_user.id)))) == 0:
            await addToBd(message)
    except Exception as ex:
        print(ex)
