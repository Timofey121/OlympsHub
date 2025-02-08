from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_lessons_notification = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информатика", callback_data='УведомПредмет-Информатика'),
            InlineKeyboardButton(text="Математика", callback_data='УведомПредмет-Математика'),
        ],
        [
            InlineKeyboardButton(text="Физика", callback_data='УведомПредмет-Физика'),
            InlineKeyboardButton(text="Химия", callback_data='УведомПредмет-Химия'),
        ],
        [
            InlineKeyboardButton(text="Биология", callback_data='УведомПредмет-Биология'),
            InlineKeyboardButton(text="География", callback_data='УведомПредмет-География'),
        ],
        [
            InlineKeyboardButton(text="История", callback_data='УведомПредмет-История'),
            InlineKeyboardButton(text="Обществознание", callback_data='УведомПредмет-Обществознание'),
        ],
        [
            InlineKeyboardButton(text="Право", callback_data='УведомПредмет-Право'),
            InlineKeyboardButton(text="Экономика", callback_data='УведомПредмет-Экономика'),
        ],
        [
            InlineKeyboardButton(text="Русский язык", callback_data='УведомПредмет-Русский язык'),
            InlineKeyboardButton(text="Английский язык", callback_data='УведомПредмет-Английский язык'),
        ],
        [
            InlineKeyboardButton(text="Французский язык", callback_data='УведомПредмет-Французский язык'),
            InlineKeyboardButton(text="Испанский язык", callback_data='УведомПредмет-Испанский язык'),
        ],
        [
            InlineKeyboardButton(text="Немецкий язык", callback_data='УведомПредмет-Немецкий язык'),
            InlineKeyboardButton(text="Литература", callback_data='УведомПредмет-Литература'),
        ],
        [
            InlineKeyboardButton(text="Лингвистика", callback_data='УведомПредмет-Лингвистика'),
            InlineKeyboardButton(text="Астрономия", callback_data='УведомПредмет-Астрономия'),
        ],
        [
            InlineKeyboardButton(text="Робототехника", callback_data='УведомПредмет-Робототехника'),
            InlineKeyboardButton(text="Технология", callback_data='УведомПредмет-Технология'),
        ],
        [
            InlineKeyboardButton(text="Искусство", callback_data='УведомПредмет-Искусство'),
            InlineKeyboardButton(text="Черчение", callback_data='УведомПредмет-Черчение'),
            InlineKeyboardButton(text="Психология", callback_data='УведомПредмет-Психология'),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в меню", callback_data='⬅️ Назад в меню'),
        ],
    ],
)
