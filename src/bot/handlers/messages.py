from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from src.bot.keyboards.reply import courses_keyboard

from src.bot.states.payment import PaymentGroup
from src.services.course import get_course_price, list_courses
from src.core import settings


COURSE_NAMES = [course.name for course in list_courses()]


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(
            send_course_invoice,
            lambda message: message.text in COURSE_NAMES,
            state=PaymentGroup.course,
            )
    dp.register_message_handler(
            wrong_course_name,
            lambda message: message.text not in COURSE_NAMES,
            state=PaymentGroup.course,
            )


async def wrong_course_name(message: types.Message, state: FSMContext):
    await message.reply(
            'Не понимаю, какой курс вы хотите приобрести. Пожалуйста, воспользуйтесь клавиатурой.\n'
            'Для отмены оплаты используйте команду /cancel',
            )


async def send_course_invoice(message: types.Message, state: FSMContext):
    course_name = message.text
    course_price = get_course_price(course_name)
    await state.update_data(course=message.text)

    await PaymentGroup.next()

    await message.reply(
            " Use this test card number to pay for your course:\n<code>1111 1111 1111 1026</code>"
            "\n\nThis is your demo invoice:",
            reply_markup=types.ReplyKeyboardRemove(),
            )

    prices = [
        types.LabeledPrice(label=f'{course_name} course', amount=course_price),
    ]
    await message.bot.send_invoice(
            message.chat.id, 
            title=course_name,
            description=f'{course_name} course in Solution',
            provider_token=settings.PAYMENTS_PROVIDER_TOKEN,
            currency='rub',
            # photo_url='https://images.fineartamerica.com/images-medium-large/2-the-time-machine-dmitriy-khristenko.jpg',
            # photo_height=512,  # !=0/None or picture won't be shown
            # photo_width=512,
            # photo_size=512,
            # is_flexible=True,  # True If you need to set up Shipping Fee
            prices=prices,
            payload=f'{course_name}',
            )

