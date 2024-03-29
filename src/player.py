from card import Card
from hand import Hand


class Player:
    def __init__(self, name: str, max_value: int) -> None:
        self.name = name
        self.max_value = max_value

        self.hand: Hand = Hand()
        self.wins = 0

        # We will collect both of the winning hand and the
        # dealers hand when the player won
        self.winning_value: list[int] = []
        self.winning_hands: list[list[Card]] = []
        self.dealers_hands: list[list[Card]] = []
        self.dealers_value: list[int] = []

    def get_value(self) -> int:
        return self.hand.get_value()

    def receive_card(self, card: Card) -> None:
        self.hand.add_card(card)

    def reset_hand(self):
        self.hand.cards_in_hand.clear()

    def won(self, dealers_hand: list[Card], dealers_value: int):
        self.wins += 1
        self.winning_value.append(self.get_value())
        self.winning_hands.append(list(self.hand.cards_in_hand))
        self.dealers_hands.append(list(dealers_hand))
        self.dealers_value.append(dealers_value)

    def __repr__(self) -> str:
        return f"{self.name} (max={self.max_value}) (wins={self.wins})"

    def __str__(self) -> str:
        return f"{self.name} (max={self.max_value}) (wins={self.wins})"
