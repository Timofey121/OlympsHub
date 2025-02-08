from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_buttons_choose_connect = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подключить")
        ],
        [
            InlineKeyboardButton(text="Не подключать")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
