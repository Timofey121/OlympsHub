import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from keyboards.inline.all_or_choice_notification import inline_buttons_choose_notification
from keyboards.inline.buttons_lessons_notification import inline_buttons_lessons_notification
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, data_olympiads, add_notification_dates, select_data_infor_id, \
    del_olympic, del_olympic_in_olympiads_parsing, select_yes_or_no_in_notifications, select_sub_id, select_tg_or_site, \
    select_sub, select_user


@dp.message_handler(text="🔔 Подключение уведомлений")
async def notification(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer(f"Привет, Olympic на связи, сейчас я тебе со всем помогу.",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(
            f"{hbold('Выберите предмет')} интересующих Вас олимпиады!",
            reply_markup=inline_buttons_lessons_notification)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")


@dp.callback_query_handler(text_startswith="УведомПредмет-")
async def notification_2(callback: types.CallbackQuery, state: FSMContext):
    subject = callback.data.split('-')[-1]
    await state.update_data(subject=subject)
    await callback.message.answer(
        'Так как не все олимпиады помогают при поступление, мы предлагаем Вам выбор(cм.ниже).',
        reply_markup=inline_buttons_choose_notification)


@dp.callback_query_handler(text_startswith="Уведомления-Вывести-")
async def info_2(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject = data.get("subject")
    answer7 = callback.from_user.id

    await callback.message.answer(hbold(f"Началось подключение уведомлений к {subject.capitalize()}!\n"
                                        f"Это займет около 2х минут"))

    sub_id = int(list(await select_sub_id(sub=str(subject).lower().capitalize()))[0][0])
    gen = list(await data_olympiads(sub_id))

    name_olimpiads = []
    stages, schedules, sites, rsochs, sub_ids = [], [], [], [], []
    dates = []

    for item in gen:
        title, start, stage, schedule, site, rsoch = item[0], item[1], item[2], item[3], item[4], item[5]
        stages.append(stage)
        schedules.append(schedule)
        sites.append(site)
        sub_ids.append(sub_id)
        name_olimpiads.append(title)
        rsochs.append(rsoch)
        dates.append(start)

    e = 0
    flag = False

    for k in range(len(name_olimpiads)):
        f = False
        if callback.data.split('-')[-1] == "все":
            f = True
        elif callback.data.split('-')[-1] == "РСОШ":
            if rsochs[k] == 1 or rsochs[k] is True:
                f = True

        if f is True:
            data = datetime.datetime.strptime(''.join(dates[k].split("-")), '%d%m%Y').date()
            now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()
            if data <= now:
                await del_olympic(name_olimpiads[k], dates[k], stages[k], schedules[k], sites[k], rsochs[k],
                                  sub_ids[k])
                await del_olympic_in_olympiads_parsing(name_olimpiads[k], dates[k], stages[k], schedules[k],
                                                       sites[k], rsochs[k], sub_ids[k])
            else:
                e += 1
                flag = True
                if len(await select_yes_or_no_in_notifications(answer7, name_olimpiads[k], dates[k],
                                                               stages[k], schedules[k], sites[k],
                                                               rsochs[k], sub_ids[k])) == 0:
                    await add_notification_dates(answer7, name_olimpiads[k], dates[k],
                                                 stages[k], schedules[k], sites[k],
                                                 rsochs[k], sub_ids[k])
    if len(name_olimpiads) == 0:
        await callback.message.answer(f"К сожалению, все олимпиады по этому предмету прошли. Уведомления  "
                                      "возможно подключить после  утверждения графика проведения олимпиад "
                                      f"школьников и их уровней "
                                      f"{datetime.datetime.now().year}/{datetime.datetime.now().year + 1} на "
                                      f"учебный год! Ориентировочно "
                                      "сентябрь-октябрь!", reply_markup=main_keyboard)
    else:
        if callback.data.split('-')[-1] == "РСОШ":
            if e == 0:
                await callback.message.answer(
                    hbold(f"К сожалению, нет таких олимпиад, которые помогут Вам при поступлении, "
                          f"посмотрите весь список олимпиад по {str(subject).capitalize()}:"),
                    reply_markup=main_keyboard)
            else:
                await callback.message.answer(hbold(f"Уведомления подключены к {subject.capitalize()}!"),
                                              reply_markup=main_keyboard)
        elif callback.data.split('-')[-1] == "все":
            await callback.message.answer(hbold(f"Подключены уведомления к {subject.capitalize()}!"),
                                          reply_markup=main_keyboard)


async def check(dp):
    dat = list(await select_data_infor_id())
    for i in range(len(dat)):
        if len(list(await select_tg_or_site(dat[i][0]))) > 0:
            tg = dat[i][0]
            subject = list(await select_sub(int(dat[i][7])))[0][0]
            information_about_olimpiad = (f"{str(subject).upper()}.  \n"
                                          f"{hunderline(dat[i][1])}.  \n"
                                          f"Начало олимпиады: {hbold(dat[i][2])} \n"
                                          f"Этап олимпиады: {hbold(dat[i][3])} \n"
                                          f"Расписание можете посмотреть {hlink(title='ТУТ!', url=dat[i][4])}\n"
                                          f"Сайт этой олимпиады Вы можете посмотреть"
                                          f"{hlink(title='ТУТ!', url=dat[i][5])}\n")

            data = datetime.datetime.strptime(''.join(dat[i][2].split("-")), '%d%m%Y').date()
            now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()

            flag = ((data - now) <= datetime.timedelta(days=2))
            flag1 = ((data - now) > datetime.timedelta(days=0))

            if flag is True and flag1 is True:
                await dp.bot.send_message(tg, f"{hbold('НЕ ЗАБУДЬТЕ!')}\n\n"
                                              f"{information_about_olimpiad}")
            else:
                if data < now:
                    await del_olympic(dat[i][1], dat[i][2], dat[i][3], dat[i][4], dat[i][5], dat[i][6], dat[i][7])
        else:
            usr = dat[i][0]
            if len(await select_user(telegram_id=usr)) > 0:
                tg = list(await select_user(telegram_id=usr))[0][0]
                subject = list(await select_sub(int(dat[i][7])))[0][0]
                information_about_olimpiad = (f"{str(subject).upper()}.  \n"
                                              f"{hunderline(dat[i][1])}.  \n"
                                              f"Начало олимпиады: {hbold(dat[i][2])} \n"
                                              f"Этап олимпиады: {hbold(dat[i][3])} \n"
                                              f"Расписание можете посмотреть {hlink(title='ТУТ!', url=dat[i][4])}\n"
                                              f"Сайт этой олимпиады Вы можете посмотреть"
                                              f"{hlink(title='ТУТ!', url=dat[i][5])}\n")

                data = datetime.datetime.strptime(''.join(dat[i][2].split("-")), '%d%m%Y').date()
                now = datetime.datetime.strptime(datetime.datetime.today().strftime('%d%m%Y'), '%d%m%Y').date()

                flag = ((data - now) <= datetime.timedelta(days=2))
                flag1 = ((data - now) > datetime.timedelta(days=0))

                if flag is True and flag1 is True:
                    await dp.bot.send_message(tg, f"{hbold('НЕ ЗАБУДЬТЕ!')}\n\n"
                                                  f"{information_about_olimpiad}")
                else:
                    if data < now:
                        await del_olympic(dat[i][1], dat[i][2], dat[i][3], dat[i][4], dat[i][5], dat[i][6], dat[i][7])
