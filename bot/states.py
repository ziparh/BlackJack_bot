from aiogram.fsm.state import State, StatesGroup

class MainDialog(StatesGroup):
    menu = State()
    game = State()
    end = State()

