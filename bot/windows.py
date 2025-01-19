from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Start, Row
from aiogram_dialog.widgets.text import Const, Format

from states import MainDialog
from game_manager import Blackjack, blackjack_getter, game_end_getter

bj = Blackjack()


async def show_balance(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    bal = '100'
    await callback.message.answer(f"Ваш баланс: {bal}")


async def show_rules(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    rules_text = """
        *Правила игры в Блэкджек:*

        1. Цель игры — набрать 21 очко или как можно ближе к этому числу.
        2. Карты с номиналом 2–10 имеют соответствующие значения. Туз может быть равен 1 или 11.
        3. Карты с буквами (J, Q, K) оцениваются как 10 очков.
        4. Игра проходит против дилера, который также старается набрать 21 очко.
        5. Для игрока доступны действия:
            - **hit** (взять дополнительную карту)
            - **stand** (остановиться с текущими картами)
        6. Если ваша сумма карт больше 21, вы проиграли.
        7. Если у дилера сумма карт больше, чем у игрока, дилер выигрывает.
        """
    await callback.message.answer(rules_text, parse_mode="Markdown")


start_window = Window(
    Const("🎲 Добро пожаловать в Блэкджек!\n\n"
          "Выберите, что вы хотите сделать:"),
    Button(Const("Начать игру"), id="play",
           on_click=lambda c, b, d: bj.start_game(d)),
    Button(Const("Посмотреть свой баланс"), id="balance", on_click=show_balance),
    Button(Const("Прочитать правила"), id="rules", on_click=show_rules),
    state=MainDialog.menu
)

game_window = Window(
    Format("Ваша ставка: {dep}\n"),
    Format("Ваша рука               Рука дилера"),
    Format("{player_hand}                     {dealer_hand}"),
    Format("Счет: {player_score}                        Счет: {dealer_score}"),
    Row(
        Button(Const("Hit"), id="hit", on_click=lambda c, b, d: bj.hit(d)),
        Button(Const("Stand"), id="stand", on_click=lambda c, b, d: bj.stand(d)),
    ),
    state=MainDialog.game,
    getter=blackjack_getter
)

game_end_window = Window(
    Format("*{wltext}*\n\n Ваша ставка была: {dep}\n Ваш {winlose} составил {wldep}"),
    Button(Const("Следущая игра"), id="next", on_click=lambda c, b, d: bj.start_game(d)),
    Button(Const("Назад в меню"), id="menu", on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),
    state=MainDialog.end,
    getter=game_end_getter
)

main_dialog = Dialog(
    start_window,
    game_window,
    game_end_window
)

