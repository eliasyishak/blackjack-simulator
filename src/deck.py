from random import randint
from random import shuffle
from typing import Literal

from card import Card
from constants import unit_deck


class Deck:
    def __init__(
        self,
        deck_type: Literal["finite", "infinite"],
        num_decks: int,
        num_shuffles: int,
    ) -> None:
        """
        This class is responsible for providing the
        necessary methods for providing cards, shuffling, etc.
        during the simulation

        deck_type: str = "finite" or "infinite"
        num_decks: int = number of decks to include; not relevant
                            if "infinite" deck_type
        num_shuffles: int = number of times to shuffle the deck
        """
        self.deck_type = deck_type
        self.num_decks = num_decks
        self.num_shuffles = num_shuffles

        # Reset the deck
        self.reset_deck()

    def deal_card(self) -> Card:
        """
        Deals from the current deck by removing the last item
        in the deck and returning it

        If infinite, will just return a random card from unit deck
        """

        if self.deck_type == "finite":
            card = self._current_deck.pop()

            # TODO: add better logic here so that we use a random point
            #       to reset the deck
            if len(self._current_deck) < 10:
                self.reset_deck()

            return card

        elif self.deck_type == "infinite":
            card = unit_deck[randint(0, len(unit_deck) - 1)]
            return card
        else:
            raise Exception("Unable to draw card, check deck_type!")

    def reset_deck(self) -> None:
        """
        This will reset the deck by creating a new list of
        decks from the unit deck and shuffling
        """

        # Define an attribute that contains all the cards
        self._current_deck: list[Card] = self.num_decks * unit_deck
        # print(f"Reset deck with {len(self._current_deck)} cards...")

        # Shuffle the deck a few times
        for _ in range(self.num_shuffles):
            shuffle(self._current_deck)
        # print(f"Finished shuffling the deck {self.num_shuffles} times...")


if __name__ == "__main__":
    deck = Deck(
        deck_type="infinite",
        num_decks=6,
        num_shuffles=5,
    )

    i = 0
    found: dict[Card, int] = {}
    while True:
        card = deck.deal_card()
        if card not in found:
            found[card] = 0
        found[card] += 1

        i += 1
        if i == 10_000:
            break

    print(found)
