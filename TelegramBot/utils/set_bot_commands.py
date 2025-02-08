from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("info", "Вывести информацию о нужной олимпиаде"),
            types.BotCommand("check_notification", "Вывести список подключенных уведомлений"),
            types.BotCommand("notification", "Подключение уведомлений"),
            types.BotCommand("delete_notification", "Удаление уведомлений"),
            types.BotCommand("secrettoken", "Получить Секретный Токен для синхронизации сайта и Телеграмм бота"),
            types.BotCommand("feedback", "Оставить отзыв"),
            types.BotCommand("technical_support", "Написать в тех поддержку!"),
        ]
    )
