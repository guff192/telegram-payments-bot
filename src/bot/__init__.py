from asyncio import get_event_loop

from aiogram import Bot, Dispatcher, types
# FIXME (uncomment): from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.bot.middlewares.logging import StateLoggingMiddleware
from src.core import settings
from .handlers import register_all_handlers 


bot = Bot(settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# TODO storage = RedisStorage()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=get_event_loop())
dp.middleware.setup(StateLoggingMiddleware())

register_all_handlers(dp)

