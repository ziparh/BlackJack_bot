import random
import asyncio

from aiogram_dialog import DialogManager

from states import MainDialog

score = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}
suits = ['❤️', '♦️', '♣️', '♠️']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()

        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        hand.append(self.deck.pop())

    def calculate_hand(self, hand):
        value = 0
        aces = 0  # Считаем количество тузов в руке

        for card in hand:
            card_value = card[:-2]
            # print(f'{card_value}: {card}, {hand}')
            value += score[card_value]

            if card_value == "A":
                aces += 1

        # Если сумма больше 21 и есть тузы, уменьшаем сумму, переводя тузы в 1
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    async def hit(self, manager: DialogManager):
        value = self.calculate_hand(self.player_hand)
        if value <= 21:
            self.deal_card(self.player_hand)
            if self.calculate_hand(self.player_hand) >= 21:
                await manager.update(data=manager.dialog_data)
                await asyncio.sleep(1)
                await self.stand(manager)
        await manager.update(data=manager.dialog_data)

    async def stand(self, manager: DialogManager):
        while self.calculate_hand(self.dealer_hand) <= self.calculate_hand(self.player_hand) and \
                    self.calculate_hand(self.player_hand) <= 21:

            self.deal_card(self.dealer_hand)
            await manager.update(data=manager.dialog_data)
            await asyncio.sleep(1)

        await self.game_end(manager)

    async def game_end(self, manager: DialogManager):
        player_value = self.calculate_hand(self.player_hand)
        dealer_value = self.calculate_hand(self.dealer_hand)

        if player_value > 21:
            manager.dialog_data['wltext'] = "Вы проиграли. У вас перебор!"
            manager.dialog_data['winlose'] = "проигрыш"
        elif dealer_value > 21:
            manager.dialog_data['wltext'] = "Вы выиграли! У дилера перебор."
            manager.dialog_data['winlose'] = "выигрыш"
        elif player_value == dealer_value:
            manager.dialog_data['wltext'] = "Ничья!"
            manager.dialog_data['winlose'] = "выигрыш"
        elif player_value == 21 and len(self.player_hand) == 2:
            manager.dialog_data['wltext'] = "Блэкджек! Вы выиграли!"
            manager.dialog_data['winlose'] = "выигрыш"
        elif dealer_value == 21 and len(self.dealer_hand) == 2:
            manager.dialog_data['wltext'] = "Вы проиграли. У дилера блэкджек."
            manager.dialog_data['winlose'] = "проигрыш"
        elif player_value > dealer_value:
            manager.dialog_data['wltext'] = f"Вы выиграли! Ваши очки: {player_value}, очки дилера: {dealer_value}."
            manager.dialog_data['winlose'] = "выигрыш"
        else:
            manager.dialog_data['wltext'] = f"Вы проиграли. Ваши очки: {player_value}, очки дилера: {dealer_value}."
            manager.dialog_data['winlose'] = "проигрыш"
        await manager.switch_to(MainDialog.end)

    async def start_game(self, manager: DialogManager):
        self.player_hand = []
        self.dealer_hand = []
        self.deal_card(self.player_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

        manager.dialog_data['player_hand'] = self.player_hand
        manager.dialog_data['dealer_hand'] = self.dealer_hand
        await manager.switch_to(MainDialog.game)
        await manager.show()
        await asyncio.sleep(1.3)

        if self.calculate_hand(self.player_hand) == 21:
            await self.game_end(manager)

bj = Blackjack()


async def blackjack_getter(dialog_manager: DialogManager, **_):
    dep = dialog_manager.dialog_data.get('dep', 0)
    player_hand = dialog_manager.dialog_data.get('player_hand')
    dealer_hand = dialog_manager.dialog_data.get('dealer_hand')
    player_score = bj.calculate_hand(player_hand)
    dealer_score = bj.calculate_hand(dealer_hand)
    print(f"dep: {dep}, player_hand: {' '.join(player_hand)}, dealer_hand: {' '.join(dealer_hand)}, "
          f"player_score: {player_score}, dealer_score: {dealer_score}")
    return {
        'dep': dep,
        'player_hand': ' '.join(player_hand),
        'dealer_hand': ' '.join(dealer_hand),
        'player_score': player_score,
        'dealer_score': dealer_score
    }


async def game_end_getter(dialog_manager: DialogManager, **_):
    wltext = dialog_manager.dialog_data.get('wltext')
    winlose = dialog_manager.dialog_data.get('winlose')
    dep = dialog_manager.dialog_data.get('dep', 0)
    wldep = dialog_manager.dialog_data.get('wldep', 0)
    return {
        'wltext': wltext,
        'winlose': winlose,
        'dep': dep,
        'wldep': wldep,
    }
