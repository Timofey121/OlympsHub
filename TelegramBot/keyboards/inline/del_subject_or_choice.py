from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить уведомления определенного предмета!",
                                 callback_data='Удалить-уведомления-предмет')
        ],
        [
            InlineKeyboardButton(text="Удалить выбранные уведомления(по номеру)!",
                                 callback_data='Удалить-уведомления-номер')
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в меню",
                                 callback_data='⬅️ Назад в меню')
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
