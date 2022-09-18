from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentTypes
from loguru import logger

from src.bot.states.payment import PaymentGroup
from src.services.course import get_course_chat_id


def register_payment_handlers(dp: Dispatcher):
    dp.register_pre_checkout_query_handler(pre_checkout, state=PaymentGroup.checkout)
    dp.register_message_handler(process_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=PaymentGroup.successful_payment)


async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await PaymentGroup.next()

    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_payment(message: types.Message, state: FSMContext):
    await PaymentGroup.next()

    data = await state.get_data()
    course_name: str = data.get('course', 'unknown')
    paid_courses: list[str] = data.get('paid_courses', [])

    price = message.successful_payment.total_amount / 100
    currency = message.successful_payment.currency
    logger.info(f'got payment {price} {currency} for {course_name} course')

    paid_courses.append(message.successful_payment.invoice_payload)
    await state.update_data(paid_courses=paid_courses)

    await message.bot.send_message(
            chat_id=message.chat.id,
            text=f'Поздравляю, вы оплатили курс {course_name}. Сумма чека:\n<code>{price} {currency}</code>'
           )


    course_chat_id = await get_course_chat_id(course_name)

    invite_link = await message.bot.create_chat_invite_link(
            course_chat_id,
            creates_join_request=True,
            )

    await message.bot.send_message(
            chat_id=message.chat.id,
            text=f'Используйте эту ссылку для добавления в чат:\n{invite_link.invite_link}',
            )



