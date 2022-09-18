from typing import Dict, Any

from fastapi import APIRouter, Body, BackgroundTasks, Response, status
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from loguru import logger

from src.bot import dp
from src.core import settings


router = APIRouter()


async def handle_update(update: Dict[str, Any]):
    '''Task for handling telegram update using aiogram'''
    telegram_update = Update(**update)
    # logger.debug(telegram_update)
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    await dp.process_update(telegram_update)


@router.post('/webhook', include_in_schema=False)
async def telegram_webhook(background_tasks: BackgroundTasks, update: Dict[str, Any] = Body()) -> Response:
    '''Webhook endpoint processing all updagtes from telegram'''
    background_tasks.add_task(handle_update, update)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.on_event('startup')
async def on_startup() -> None:
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)

    current_url = (await dp.bot.get_webhook_info())['url'] 
    if current_url != settings.WEBHOOK_URL + settings.WEBHOOK_PATH:
        await dp.bot.set_webhook(
                url=settings.WEBHOOK_URL + settings.WEBHOOK_PATH,
                secret_token=settings.SECRET,
                drop_pending_updates=True,
                )

    await dp.bot.send_message(chat_id=settings.ADMIN, text='Bot successfully started')


@router.on_event('shutdown')
async def on_shutdown() -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()

    # check if session exists
    session = await dp.bot.get_session()
    if session:
        await session.close()

