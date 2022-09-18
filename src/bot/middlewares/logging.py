from loguru import logger

from aiogram import Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware


HANDLED_STR = ['Unhandled', 'Handled']


class StateLoggingMiddleware(BaseMiddleware):
    def __init__(self):
        self.logger = logger
        self.logger.debug('Set up middleware')

        super(StateLoggingMiddleware, self).__init__()
    
    async def _log_current_state_with_data(self, chat_id: int, user_id: int):
        dp = Dispatcher.get_current()

        state = dp.current_state(chat=chat_id, user=user_id)
        current_state = await state.get_state()
        data = await state.get_data()

        self.logger.debug(f'{current_state=} {data=}\n')

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        chat_id = message.chat.id
        await self._log_current_state_with_data(chat_id, chat_id)

    async def on_post_process_pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery, results, data: dict):
        chat_id = pre_checkout_query.from_user.id
        self.logger.debug(f'{HANDLED_STR[bool(len(results))]} pre-checkout query [ID:{pre_checkout_query.id}] from user [ID:{chat_id}]')
        await self._log_current_state_with_data(chat_id, chat_id)

    async def trigger(self, action, args):
        self.logger.debug(f'{action=}:')

        update_object: types.Update = args[0]
        if hasattr(update_object, 'text'):
            message_text: str = update_object.text
        else:
            message_text = 'No text'
        self.logger.debug(f'text: {message_text}')

        await super(StateLoggingMiddleware, self).trigger(action, args)

