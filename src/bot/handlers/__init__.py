from aiogram import Dispatcher

from .commands import register_command_handlers
from .payments import register_payment_handlers
from .messages import register_message_handlers
from .chat import register_chat_handlers


def register_all_handlers(dp: Dispatcher):
    register_command_handlers(dp)
    register_payment_handlers(dp)
    register_message_handlers(dp)
    register_chat_handlers(dp)

