from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loguru import logger
from src.bot.states.payment import PaymentGroup

from src.bot.keyboards.reply import courses_keyboard 


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'], state='*') 
    dp.register_message_handler(buy, commands=['buy'], state='*')
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')


async def start(message: types.Message):
    '''
    Send user help message
    '''
    await message.reply(
            'This bot is for testing payments (or anything else)'
            '\nTry using /buy command to test payments',
            reply_markup=types.ReplyKeyboardRemove(),
            )


async def buy(message: types.Message):
    '''
    Start course selling process. Sets current state to PaymentGroup:course
    '''
    await message.reply(
            'Выберите курс, который хотите купить', 
            reply_markup=courses_keyboard,
            )

    # Set state
    await PaymentGroup.course.set()


async def cancel_handler(message: types.Message, state: FSMContext):
    '''
    Allow user to cancel any action
    '''
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('Nothing to cancel')
        return

    logger.info(f'Cancelling state {current_state}')
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
