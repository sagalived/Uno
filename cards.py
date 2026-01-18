import random

COLORS = ["red", "green", "blue", "yellow"]
SPECIALS = ["skip", "reverse", "+2"]

def create_deck():
    deck = []
    for color in COLORS:
        for n in range(10):
            deck.append((str(n), color))
            if n != 0: deck.append((str(n), color))
        for s in SPECIALS:
            deck.append((s, color))
            deck.append((s, color))
    for _ in range(4):
        deck.append(("+4", "wild"))
    random.shuffle(deck)
    return deck

def can_play(top_card, card):
    v, c = card
    tv, tc = top_card
    return c == "wild" or c == tc or v == tv