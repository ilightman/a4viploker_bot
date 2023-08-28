import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from filters import UserNotBanned
from handlers.users.users import register_user_handlers
from middlewares.ban_mw import BanMiddleware
from middlewares.throttling_aiogram import ThrottlingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


def register_all_handlers(disp: Dispatcher):
    disp.filters_factory.bind(UserNotBanned)

    register_user_handlers(disp)


register_all_handlers(dp)


async def set_default_commands(disp: Dispatcher):
    await disp.bot.set_my_commands([
        types.BotCommand("start", "Начать работу"),
        types.BotCommand("help", "Помощь"),
    ])


async def on_startup(disp: Dispatcher):
    await set_default_commands(disp)
    disp.middleware.setup(ThrottlingMiddleware())
    disp.middleware.setup(BanMiddleware())

    logging.warning('Бот запущен и работает')


async def on_shutdown(disp: Dispatcher):
    await disp.storage.close()
    await disp.storage.wait_closed()
    logging.warning('Бот выключается')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
