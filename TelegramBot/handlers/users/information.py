# -*- coding: utf8 -*-
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from keyboards.inline.all_or_choice import inline_buttons_choose
from keyboards.inline.buttons_lessons import inline_buttons_lessons
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, information_about_olympiads, del_olympic, \
    del_olympic_in_olympiads_parsing, select_sub_id


@dp.message_handler(text='✍️ Вывести информацию о нужной олимпиаде')
async def info(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer(f"Привет, Olympic на связи, сейчас я тебе со всем помогу.",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(
            f"{hbold('Выберите предмет')} интересующих Вас олимпиады!", reply_markup=inline_buttons_lessons)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.callback_query_handler(text_startswith="⬅️ Назад в меню")
async def deal_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы вернулись в меню', reply_markup=main_keyboard)


@dp.callback_query_handler(text_startswith="ИнфорПредмет-")
async def info_1(callback: types.CallbackQuery, state: FSMContext):
    subject = callback.data.split('-')[-1]
    await state.update_data(subject=subject)
    await callback.message.answer(
        'Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
        reply_markup=inline_buttons_choose)


@dp.callback_query_handler(text_startswith="Информация-Вывести-")
async def info_2(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject = data.get("subject")
    await callback.message.answer(
        hbold(f"Подождите немного!\nНачался поиск информации об {subject.capitalize()}!\n"
              f"Это займет около 2х минут"))

    sub_id = int(list(await select_sub_id(sub=str(subject).lower().capitalize()))[0][0])
    gen = list(await information_about_olympiads(sub_id))

    name_olimpiads = []
    information_olimpiads = []
    stages, schedules, sites, rsochs, sub_ids = [], [], [], [], []
    dates = []

    for item in gen:
        title, start, stage, schedule, site, rsoch = item[0], item[1], item[2], item[3], item[4], item[5]
        stages.append(stage)
        schedules.append(schedules)
        sites.append(site)
        sub_ids.append(sub_id)
        name_olimpiads.append(title)
        rsochs.append(rsoch)
        information_about_olimpiad = (f"{hunderline(title)}.  \n"
                                      f"Начало олимпиады: {hbold(start)} \n"
                                      f"Этап олимпиады: {hbold(stage)} \n"
                                      f"Расписание можете посмотреть {hlink(title='ТУТ!', url=schedule)}\n"
                                      f"Сайт этой олимпиады Вы можете посмотреть"
                                      f"{hlink(title='ТУТ!', url=site)}\n")
        information_olimpiads.append(information_about_olimpiad)
        dates.append(start)

    count = 0
    count_1 = 0
    flag = False

    for k in range(len(name_olimpiads)):
        f = False

        if callback.data.split('-')[-1] == "все":
            f = True
        elif callback.data.split('-')[-1] == "РСОШ":
            f = rsochs[k]
            count_1 += 1

        if f is True or f == 1:
            if datetime.datetime.strptime(''.join(dates[k].split("-")),
                                          '%d%m%Y').date() <= datetime.datetime.strptime(
                datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date():
                await del_olympic(name_olimpiads[k], dates[k], stages[k], schedules[k], sites[k], rsochs[k],
                                  sub_ids[k])
                await del_olympic_in_olympiads_parsing(name_olimpiads[k], dates[k], stages[k], schedules[k],
                                                       sites[k], rsochs[k], sub_ids[k])
            else:
                count += 1
                await callback.message.answer(f"{count}) {information_olimpiads[k]}", reply_markup=main_keyboard)

    if len(name_olimpiads) == 0:
        await callback.message.answer('К сожалению, все олимпиды по этому предмету в этом учебном году прошли!',
                                      reply_markup=main_keyboard)
    else:
        await callback.message.answer(
            hbold("Олимпиады упрощают поступление в ВУЗ! Они позволяют "
                  "поступить в ВУЗ без экзаменов или засчитать 100 баллов по ЕГЭ."))
        await callback.message.answer(
            hbold("Не забывайте, что ЕГЭ — это всего одна попытка. Олимпиад много "
                  "и количество раз, "
                  "которое вы попробуете, зависит только от вас. Тут работает теория вероятностей"
                  " — чем больше пробуешь, тем выше шансы на успех."))
        await callback.message.answer(
            hbold("По статистике каждый школьник забывает примерно о 6 из 10 олимпиад, из-за этого"
                  " снижается шанс поступления в ВУЗ. Поэтому мы предлагаем Вам, бесплатно "
                  "подключить уведомления на "
                  "разные олимпиады, хотите подключить уведомления?"), reply_markup=main_keyboard)
