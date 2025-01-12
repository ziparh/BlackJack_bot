import random


suits = ['❤️', '♦️', '♣️', '♠️']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
random.shuffle(deck)