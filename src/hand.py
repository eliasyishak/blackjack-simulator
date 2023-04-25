from card import Card


class Hand:
    def __init__(self) -> None:
        self.cards_in_hand: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards_in_hand.append(card)

    def get_value(self) -> int:
        """
        This function will return the value of the
        given hand, it will always return the soft value
        if possible

        For example, if an Ace and a 5 were dealt, it will
        return a value of 16, but if another card is dealt with
        a value of 8, it will automatically adjust to 14
        """

        # Initialize the value of the hand and
        # a counter for the number of aces in hand
        value = 0
        aces_count = 0

        for card in self.cards_in_hand:
            if card.rank in ["J", "Q", "K"]:
                value += 10
            elif card.rank in ["A"]:
                value += 11
                aces_count += 1
            else:
                value += int(card.rank)

        # This loop will ensure that we take the minimum
        # value of 1 for an ace if we have busted
        while aces_count > 0 and value > 21:
            value -= 10
            aces_count -= 1

        return value

    def __repr__(self) -> str:
        return f"Hand Value: {self.get_value()}"

    def __str__(self) -> str:
        return f"Hand Value: {self.get_value()}"


if __name__ == "__main__":
    hand = Hand()

    print(hand)
