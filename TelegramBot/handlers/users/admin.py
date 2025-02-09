from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from data.config import ADMINS
from keyboards.default.admin_commands import keyboard_4
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.v_menu import buttons_menu
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import select_all_users, select_data_olimp_use_id, count_users, select_blocked_users, \
    update_blocked_users, subscriber_exists, all_tech_failed, del_tech, all_feedback, del_feedback, \
    select_subjects_olimp_use_id, count_olympiads


@dp.message_handler(Command("admin"))
async def notification(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Выберите нужную команду (cм.ниже).', reply_markup=keyboard_4)
        await Test.Q_for_admin_1.set()
    else:
        text = ("ТАКОЙ КОМАНДЫ НЕТ!", "Список команд: ", "/start - Начать диалог",
                "/info - Вывести информацию о нужной олимпиаде", "/notification - Подключение уведомлений",
                "/check_notification - Подключение уведомлений", "/delete_notification - Удаление уведомлений",
                "/feedback - Оставить отзыв", "/technical_support - Написать в тех поддержку!",
                "/help - Получить справку",)

        await message.answer("\n".join(text))


@dp.message_handler(state=Test.Q_for_admin_1)
async def answer(message: types.Message, state: FSMContext):
    try:
        if message.text == "Показать уведомления пользователей!":
            dat = list(await select_all_users())
            for i in range(len(dat)):
                g = []
                for item in (list(set(list(await select_subjects_olimp_use_id(dat[i][0]))))):
                    g.append(item[0])
                await message.answer(
                    f"У пользователя {dat[i][1]} подключено {len(await select_data_olimp_use_id(dat[i][0]))} "
                    f"уведомления к олимпиадам. По предметам: {' '.join(g)}", reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Показать полный список пользователей!":
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Показать кол-во пользователей!":
            await message.answer(f"Привет админ! В боте - {list(await count_users())[0][0]} пользователей!",
                                 reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Заблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=buttons_menu)
            await Test.Q_for_admin_2.set()

        elif message.text == "Разблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_blocked_users())
            c = [[]]
            t = 0
            if len(dat) == 0:
                await message.answer(f'Заблокированных пользователей нет!', reply_markup=main_keyboard)
                await state.finish()
            else:
                await message.answer(f"Полный список заблокированных пользователей:")
                for i in range(len(dat)):
                    if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")
                for i in range(len(c)):
                    await message.answer("\n".join(c[i]), reply_markup=buttons_menu)
                await Test.Q_for_admin_3.set()

        elif message.text == "Отправить пользователям сообщение!":
            await message.answer(f"Введите сообщение для пользователей!", reply_markup=buttons_menu)
            await Test.Q_for_admin_4.set()

        elif message.text == "Посмотреть все технические ошибки!":
            dat = list(await all_tech_failed())
            c = [[]]
            t = 0
            if len(dat) == 0:
                await message.answer(f'Обращений пока не было.', reply_markup=main_keyboard)
            else:
                await message.answer(f"Полный список технических ошибок:")
                for i in range(len(dat)):
                    if len(str(f"Пользователь @{dat[i][0]} \nОбращение:\n {hbold(dat[i][1])}\n")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"Пользователь @{dat[i][0]} \nОбращение:\n  {hbold(dat[i][1])}\n")
                for i in range(len(c)):
                    await message.answer("\n".join(c[i]), reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Удалить выполненные тех. ошибки!":
            dat = list(await all_tech_failed())
            c = [[]]
            a = 0
            t = 0
            if len(dat) == 0:
                await message.answer(f"Обращений пока нет!", reply_markup=main_keyboard)
                await state.finish()
            else:
                await message.answer(f"Полный список технических ошибок:")
                for i in range(len(dat)):
                    a += 1
                    if len(str(f"{a}) Пользователь @{dat[i][0]} \nОбращение:\n {hbold(dat[i][1])}\n")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"{a}) Пользователь @{dat[i][0]} \nОбращение:\n  {hbold(dat[i][1])}\n")
                for i in range(len(c)):
                    await message.answer("\n".join(c[i]), reply_markup=ReplyKeyboardRemove())
                await message.answer(f"Введите номер обращения, которое нужно удалить.", reply_markup=buttons_menu)
                await Test.Q_for_admin_5.set()

        elif message.text == 'Посмотреть все отзывы!':
            dat = list(await all_feedback())
            c = [[]]
            a = 0
            t = 0
            if len(dat) == 0:
                await message.answer(f"Отзывов пока нет!", reply_markup=main_keyboard)
            else:
                await message.answer(f"Полный список отзывов:")
                for i in range(len(dat)):
                    a += 1
                    if len(str(f"{a}) Пользователь @{dat[i][0]} \nЕго отзыв:\n {hbold(dat[i][1])}\n")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"{a}) Пользователь @{dat[i][0]} \nЕго отзыв:\n {hbold(dat[i][1])}\n")
                for i in range(len(c)):
                    await message.answer("\n".join(c[i]), reply_markup=main_keyboard)
            await state.finish()

        elif message.text == 'Отчистить БД от отзывов!':
            await del_feedback()
            await message.answer('База данных отчищена!', reply_markup=main_keyboard)
            await state.finish()

        elif message.text == 'Количество олимпиад в Базе Данных!':
            try:
                f = open('additional_files/log.txt').read().split(';')
                await message.answer(f'{f[0]}\nПоследние изменения в БД с олимпиадами.\nВ Бд '
                                     f'{list(await count_olympiads())[0][0]} строк!\nВремя выполнения: {f[1]}',
                                     reply_markup=main_keyboard)
                await state.finish()
            except Exception as ex:
                print(ex)

    except Exception as ex:
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_5)
async def block1(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        dat = list(await all_tech_failed())
        a, b = dat[int(message.text) - 1]
        await del_tech(a, b)
        await message.answer(f"Техническая ошибка под номером {message.text} - удалена.", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_2)
async def block2(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            await update_blocked_users(message.text, 1)
            await message.answer(
                f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - ЗАБЛОКИРОВАН",
                reply_markup=main_keyboard)
        except Exception as ex:
            print(ex)
            await message.answer("Такого пользователя не существует!", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_3)
async def block3(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            await update_blocked_users(message.text, 0)
            await message.answer(
                f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - РАЗБЛОКИРОВАН",
                reply_markup=main_keyboard)
        except:
            await message.answer("Такого пользователя не существует!", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_4)
async def block4(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        dat = list(await select_all_users())
        for i in range(len(dat)):
            try:
                await dp.bot.send_message(f'{dat[i][1]}', message.text)
            except:
                pass
        await state.finish()
