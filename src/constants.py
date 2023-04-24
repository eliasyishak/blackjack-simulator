from card import Card


# The face values of the cards
face_values: list[str] = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
]

# The suits for each card
suits: list[str] = ["Clubs", "Spades", "Diamonds", "Hearts"]

# Combine the above 2 lists to get a deck of 52 cards
unit_deck: list[Card] = []
for suit in suits:
    for val in face_values:
        unit_deck.append(Card(rank=val, suit=suit))
