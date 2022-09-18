from aiogram.dispatcher.filters.state import State, StatesGroup


class PaymentGroup(StatesGroup):
    course = State()
    checkout = State()
    successful_payment = State()
    join_request = State()

