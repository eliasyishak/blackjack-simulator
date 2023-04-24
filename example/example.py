import random
from typing import List


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        ranks = [str(i) for i in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.cards: List[Card] = [Card(rank, suit) for suit in suits for rank in ranks]
        print(self.cards)
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank in ["Jack", "Queen", "King"]:
                value += 10
            elif card.rank == "Ace":
                num_aces += 1
                value += 11
            else:
                value += int(card.rank)
        while num_aces > 0 and value > 21:
            value -= 10
            num_aces -= 1
        return value

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def play(self):
        self.deal_initial_cards()
        print(f"Player's hand: {self.player_hand}")
        print(f"Dealer's hand: {self.dealer_hand.cards[0]}")
        while True:
            if self.player_hand.get_value() > 21:
                print("Bust! You lose.")
                return
            elif self.player_hand.get_value() == 21:
                print("Blackjack! You win!")
                return
            hit_or_stand = input("Hit or stand? ")
            if hit_or_stand.lower() == "hit":
                self.player_hand.add_card(self.deck.deal_card())
                print(f"Player's hand: {self.player_hand}")
            elif hit_or_stand.lower() == "stand":
                break
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        print(f"Dealer's hand: {self.dealer_hand}")
        if self.dealer_hand.get_value() > 21:
            print("Dealer busts! You win!")
        elif self.dealer_hand.get_value() > self.player_hand.get_value():
            print("Dealer wins!")
        elif self.dealer_hand.get_value() < self.player_hand.get_value():
            print("You win!")
        else:
            print("Push (tie)!")


if __name__ == "__main__":
    game = Blackjack()
    game.play()
