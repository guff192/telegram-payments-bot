from typing import List
from loguru import logger

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import StateFilter

from src.bot.states.payment import PaymentGroup
from src.services.course import get_course_chat_id, get_course_name_by_chat_id


def register_chat_handlers(dp: Dispatcher):
    dp.register_chat_join_request_handler(handle_join_request)


async def handle_join_request(chat_join_request: types.ChatJoinRequest):
    logger.debug('got join request')

    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id
    course_name = await get_course_name_by_chat_id(chat_id)

    dp = Dispatcher.get_current()
    personal_chat_state = dp.current_state(chat=user_id, user=user_id)
    data = await personal_chat_state.get_data()

    paid_courses: List[str] = data.get('paid_courses', [])
    if not paid_courses or course_name not in paid_courses:
        await chat_join_request.bot.decline_chat_join_request(
                chat_id=chat_id,
                user_id=user_id,
                )
        logger.info(f'declined user {user_id} to join chat {chat_id}')
        return

    await chat_join_request.bot.approve_chat_join_request(
            chat_id=chat_id,
            user_id=user_id,
            )
    logger.info(f'accepted user {user_id} to join chat {chat_id}')


