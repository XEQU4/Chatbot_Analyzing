from aiogram.fsm.state import State, StatesGroup


class FSM(StatesGroup):
    query_waiting = State()
    first_answer_waiting = State()
    second_answer_waiting = State()
    third_answer_waiting = State()
    contact_waiting = State()
    passed = State()
