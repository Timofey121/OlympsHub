from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # подключение модуля MemoryStorage - запоминать состояния
from data import config  # подключение модуля, хранящего данные

bot = Bot(token=config.BOT_TOKEN,
          parse_mode=types.ParseMode.HTML)  # подключение к боту через TOKEN, полученным через BotFather
storage = MemoryStorage()  # создание метода состояний
dp = Dispatcher(bot, storage=storage)  # создание Dispatcher - принимает все запросы и обрабатывает их
