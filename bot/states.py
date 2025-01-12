from aiogram.fsm.state import State, StatesGroup

class MainDialog(StatesGroup):
    start = State()
    rules = State()
    play = State()

class BlackJackDialog(StatesGroup):
    main = State()

