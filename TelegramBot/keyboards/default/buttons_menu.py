from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑🏻‍💻 Get Secret Token for website and Telegram bot synchronization"),
        ],
        [
            KeyboardButton(text="✍️ Get information about the olympiad you need"),
        ],
        [
            KeyboardButton(text="🔔 View connected notifications")
        ],
        [
            KeyboardButton(text="🔔 Connect notifications"),
            KeyboardButton(text="🔔 Remove notifications"),
        ],
        [
            KeyboardButton(text="📝 Leave feedback"),
            KeyboardButton(text="📝 Contact technical support"),
        ],
    ],
    resize_keyboard=True  # button size (not huge)
)
