from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='ИнфорПредмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='ИнфорПредмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='ИнфорПредмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='ИнфорПредмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='ИнфорПредмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='ИнфорПредмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='ИнфорПредмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='ИнфорПредмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='ИнфорПредмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='ИнфорПредмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='ИнфорПредмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='ИнфорПредмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='ИнфорПредмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='ИнфорПредмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='ИнфорПредмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='ИнфорПредмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='ИнфорПредмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='ИнфорПредмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='ИнфорПредмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='ИнфорПредмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='ИнфорПредмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='ИнфорПредмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='ИнфорПредмет-Психология'),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в меню", callback_data='⬅️ Назад в меню'),
        ],
    ],
)
