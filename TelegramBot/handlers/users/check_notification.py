from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink, hunderline, hbold

from loader import dp
from utils.db_api.PostgreSQL import select_data_sub_info, subscriber_exists, select_user, select_sub


@dp.message_handler(text="🔔 Просмотр подключенных уведомлений")
async def check_notification(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer("Подождите немного! Начался поиск Ваших уведомлений!")
        try:
            a = list(await select_data_sub_info(telegram_id=message.from_user.id))
            if len(await select_user(telegram_id=message.from_user.id)) > 0:
                a += list(await select_data_sub_info(
                    telegram_id=list(await select_user(telegram_id=message.from_user.id))[0][-1]))
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
                    if information_about_olimpiad not in b:
                        b.append(information_about_olimpiad)
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
                            k = 0
                            c[t].append(f"{hbold(str(subject).upper())}\n\n{k + 1}) Уведомления подключены к \n{information_about_olimpiad}")
                            subs.append(subject)
                        else:
                            c[t].append(f"{k + 1}) Уведомления подключены к \n{information_about_olimpiad}")
                        k += 1

                for i in range(len(c)):
                    await message.answer("\n".join(c[i]))
            else:
                await message.answer(
                    "К сожалению, у Вас не подключены уведомления")
        except Exception as ex:
            print(ex)
            await message.answer(
                "К сожалению, у Вас не подключены уведомления")
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")
