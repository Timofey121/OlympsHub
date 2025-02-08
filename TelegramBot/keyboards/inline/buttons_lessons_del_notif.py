from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons_delete_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='УдалУвеПредмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='УдалУвеПредмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='УдалУвеПредмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='УдалУвеПредмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='УдалУвеПредмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='УдалУвеПредмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='УдалУвеПредмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='УдалУвеПредмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='УдалУвеПредмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='УдалУвеПредмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='УдалУвеПредмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='УдалУвеПредмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='УдалУвеПредмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='УдалУвеПредмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='УдалУвеПредмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='УдалУвеПредмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='УдалУвеПредмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='УдалУвеПредмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='УдалУвеПредмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='УдалУвеПредмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='УдалУвеПредмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='УдалУвеПредмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='УдалУвеПредмет-Психология'),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в меню", callback_data='⬅️ Назад в меню'),
        ],
    ],
)
