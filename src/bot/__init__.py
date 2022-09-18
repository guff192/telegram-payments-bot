from asyncio import get_event_loop

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.bot.middlewares.logging import StateLoggingMiddleware
from src.core import settings
from .handlers import register_all_handlers 


# TODO storage = RedisStorage()
bot = Bot(settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=get_event_loop())
dp.middleware.setup(StateLoggingMiddleware())

register_all_handlers(dp)

