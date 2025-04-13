from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    name = State()
    phone = State()


from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    category_id = State()
    amount = State()
    prepayment_amount = State()
    new_prepayment_amount = State()
