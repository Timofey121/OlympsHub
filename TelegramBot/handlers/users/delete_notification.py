# -*- coding: utf8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink, hunderline

from keyboards.default.buttons_menu import main_keyboard
from keyboards.inline.buttons_lessons_del_notif import inline_buttons_lessons_delete_notification
from keyboards.inline.del_subject_or_choice import inline_buttons_delete
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import select_data_olimp_use_id, subscriber_exists, select_data_sub_info, \
    del_notif_in_olimpic, select_user, select_sub, del_data_in_olimpic, select_sub_id, select_data_olimp_use_subject


@dp.message_handler(text="🔔 Удаление уведомлений")
async def del_notification(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer(f"Привет, Olympic на связи, сейчас я тебе со всем помогу.",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите способ удаления уведомлений(cм.ниже).', reply_markup=inline_buttons_delete)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.callback_query_handler(text_startswith="Удалить-уведомления-")
async def info_1(callback: types.CallbackQuery, state: FSMContext):
    answer_1 = callback.data.split('я-')[-1]
    await state.update_data(answer1=answer_1)
    if answer_1 == "предмет":
        try:
            if len(list(await select_data_olimp_use_id(telegram_id=callback.from_user.id))) > 0:
                await callback.message.answer(
                    f"{hbold('Выберите предмет')} интересующих Вас олимпиады!",
                    reply_markup=inline_buttons_lessons_delete_notification)
            else:
                await callback.message.answer("Перед тем, чтобы удалять уведомления, их надо подключить",
                                              reply_markup=main_keyboard)
        except Exception as ex:
            await callback.message.answer("Перед тем, чтобы удалять уведомления, их надо подключить",
                                          reply_markup=main_keyboard)

    elif answer_1 == "номер":
        await callback.message.answer("Подождите немного! Начался поиск уведомлений!")
        a = list(await select_data_sub_info(telegram_id=callback.from_user.id))
        if len(await select_user(telegram_id=callback.from_user.id)) > 0:
            a += list(await select_data_sub_info(
                telegram_id=list(await select_user(telegram_id=callback.from_user.id))[0][-1]))
        c = [[]]
        t, k = 0, 0
        subs = []
        b = []
        if len(a) > 0:
            for i in range(len(a)):
                information_about_olimpiad = ''
                subject = list(await select_sub(int(a[i][-1])))[0][0]
                information_about_olimpiad += (f"{hunderline(a[i][1])}.  \n"
                                               f"Начало олимпиады: {hbold(a[i][2])} \n"
                                               f"Этап олимпиады: {hbold(a[i][3])} \n")
                i_about_ol = [a[i][1], a[i][2], a[i][3], a[i][-1]]
                if i_about_ol not in b:
                    b.append(i_about_ol)
                    information_about_olimpiad += "Олимпиада "
                    if a[i][-2] is True or str(a[i][-2]) == '1':
                        information_about_olimpiad += hbold('Входит в РСОШ')
                    else:
                        information_about_olimpiad += hbold('НЕ входит в РСОШ')
                    information_about_olimpiad += (
                        f"\nРасписание можете посмотреть {hlink(title='ТУТ!', url=a[i][4])}\n"
                        f"Сайт этой олимпиады Вы можете посмотреть {hlink(title='ТУТ!', url=a[i][5])}\n")
                    if len(str(
                            subject).upper() + f"{k + 1}) Уведомления подключены к \n\n" + information_about_olimpiad
                           + '\n' + '-' * 54) > 4096:
                        t += 1
                        c.append([])
                    if subject not in subs:
                        c[t].append('~' * 54)
                        c[t].append(
                            f"{hbold(str(subject).upper())}\n\n{k + 1}) Уведомления подключены к \n{information_about_olimpiad}")
                        subs.append(subject)
                    else:
                        c[t].append(f"{k + 1}) Уведомления подключены к \n{information_about_olimpiad}")
                    k += 1
            for i in range(len(c)):
                await callback.message.answer("\n".join(c[i]))
        await callback.message.answer(
            "Введите номера тех олимпиад, уведомления которых Вы хотите удалить(через запятую)!")
        await Test.Q_for_delete_notification_2.set()


@dp.callback_query_handler(text_startswith="УдалУвеПредмет-")
async def idelnotif34(callback: types.CallbackQuery, state: FSMContext):
    sa = callback.data.split("-")[-1]
    sub_id = int(list(await select_sub_id(sub=(str(sa).lower().capitalize())))[0][0])
    rgt = list(await select_data_olimp_use_subject(sub_id))

    if rgt:
        await callback.message.answer(
            hbold(f"Началось отключение уведомлений, подключенных к {sa.capitalize()}!"))
        await del_data_in_olimpic(customer=callback.from_user.id, sub_id=sub_id)
        if len(await select_user(telegram_id=callback.from_user.id)) > 0:
            await del_data_in_olimpic(customer=list(await select_user(telegram_id=callback.from_user.id))[0][-1],
                                      sub_id=sub_id)
        await callback.message.answer(hbold(f"Отключены уведомления, подключенные к {sa.capitalize()}!"),
                                      reply_markup=main_keyboard)
    else:
        await callback.message.answer(hbold(f"Уведомления не подключены к {sa.capitalize()}"),
                                      reply_markup=main_keyboard)


@dp.message_handler(state=Test.Q_for_delete_notification_2)
async def del_notification_2(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    try:
        sa = message.text.split(",")
        for i in range(len(sa)):
            sa[i] = str(sa[i]).lstrip().rstrip()
        a = list(await select_data_sub_info(telegram_id=message.from_user.id))
        if len(await select_user(telegram_id=message.from_user.id)) > 0:
            a += list(await select_data_sub_info(
                telegram_id=list(await select_user(telegram_id=message.from_user.id))[0][-1]))
        b = []
        for i in range(len(a)):
            i_about_ol = [a[i][1], a[i][2], a[i][3], a[i][4], a[i][5], a[i][-1]]
            if i_about_ol not in b:
                b.append(i_about_ol)
        for i in range(len(b)):
            if str(int(i + 1)) in sa:
                information_about_olimpiad = ''
                information_about_olimpiad += (f"{hunderline(b[i][0])}.  \n"
                                               f"Начало олимпиады: {hbold(b[i][1])} \n"
                                               f"Этап олимпиады: {hbold(b[i][2])} \n")
                information_about_olimpiad += "Олимпиада "
                information_about_olimpiad += (
                    f"\nРасписание можете посмотреть {hlink(title='ТУТ!', url=b[i][3])}\n"
                    f"Сайт этой олимпиады Вы можете посмотреть {hlink(title='ТУТ!', url=b[i][4])}\n")
                await del_notif_in_olimpic(telegram_id, b[i][0], b[i][1],
                                           b[i][2], b[i][4], b[i][5])
                if len(await select_user(telegram_id=message.from_user.id)) > 0:
                    await del_notif_in_olimpic(list(await select_user(telegram_id=message.from_user.id))[0][-1],
                                               b[i][0], b[i][1],
                                               b[i][2], b[i][4], b[i][5])
                await message.answer("Уведомления отключены от")
                await message.answer(f"{i + 1}) {information_about_olimpiad}", reply_markup=main_keyboard)
    except Exception as ex:
        await message.answer(f"Проверьте правильность номеров уведомлений, для удаления!", reply_markup=main_keyboard)
    await state.finish()
