import random as r
from typing import Union

import constants
from deck import Deck
import pandas as pd
from player import Player
from tqdm import tqdm


# Seed to reproduce runs
r.seed(5128)

# Define how many players to use in the simulation along
# with the max number they won't pass
#
# ie. a player with a max number of 18 won't hit if they
# have a hand value of 18 or more
PLAYERS: list[Player] = [
    Player(name="A", max_value=15),
    Player(name="B", max_value=16),
    Player(name="C", max_value=17),
    Player(name="D", max_value=18),
    Player(name="E", max_value=19),
    Player(name="F", max_value=20),
    Player(name="G", max_value=21),
]
dealer: Player = Player(name="Dealer", max_value=17)

# Define the constants for the simulation
GAMES = 1_000_000
TQDM_DISABLED = False

# Iterate through the number of runs specified
for _ in tqdm(range(GAMES), disable=TQDM_DISABLED):
    # Shuffle the players so that we vary who starts the game
    # current_players = [obj for obj in players]
    current_players = list(PLAYERS)
    r.shuffle(current_players)

    # Initialize the deck
    deck = Deck(deck_type="infinite", num_decks=6, num_shuffles=5)

    # Deal the first two cards to each player + dealer
    for game_player in current_players + [dealer]:
        game_player.receive_card(deck.deal_card())
        game_player.receive_card(deck.deal_card())

    # Iterate through each player for the full game
    for player in current_players:
        # While loop used to continue playing the game
        # until each players max or greater
        while player.get_value() < player.max_value:
            player.receive_card(deck.deal_card())

    # Seprate while loop for the dealer's turn to deal himself
    while dealer.get_value() < dealer.max_value:
        dealer.receive_card(deck.deal_card())

    # Check if each player won the game
    for player in current_players:
        # When the dealer busts and the player has a valid hand
        if dealer.get_value() > 21 and player.get_value() <= 21:
            player.won(
                dealers_hand=list(dealer.hand.cards_in_hand),
                dealers_value=dealer.get_value(),
            )
        # When the dealer has less than the player and the player has a
        # valid hand
        elif player.get_value() > dealer.get_value() and player.get_value() <= 21:
            player.won(
                dealers_hand=list(dealer.hand.cards_in_hand),
                dealers_value=dealer.get_value(),
            )
        else:
            dealer.won(
                dealers_hand=list(dealer.hand.cards_in_hand),
                dealers_value=dealer.get_value(),
            )

    # Reset the hand for each player after their game is over
    for game_player in current_players + [dealer]:
        game_player.reset_hand()

# Generate a spreadsheet to analyze the results
output_obj: dict[str, list[Union[str, int]]] = {
    "player": [],
    "max_value": [],
    "first_two_hand": [],
    "winning_value": [],
    "cards_in_hand": [],
    "first_dealer_card": [],
    "dealer_value": [],
    "dealer_hand": [],
}
for player in tqdm(PLAYERS, disable=TQDM_DISABLED):
    assert (
        len(player.winning_value)
        == len(player.winning_hands)
        == len(player.dealers_hands)
        == len(player.dealers_value)
    )

    for index in range(len(player.winning_value)):
        # Calculate the values needed
        first_two_cards: str = ", ".join(
            [card.rank for card in player.winning_hands[index][0:2]]
        )
        cards_in_hand: str = ", ".join(
            [card.rank for card in player.winning_hands[index]]
        )
        dealer_hand: str = ", ".join(
            [card.rank for card in player.dealers_hands[index]]
        )

        # Extract the values from the class
        output_obj["player"].append(player.name)
        output_obj["max_value"].append(player.max_value)
        output_obj["first_two_hand"].append(first_two_cards)
        output_obj["winning_value"].append(player.winning_value[index])
        output_obj["cards_in_hand"].append(cards_in_hand)
        output_obj["first_dealer_card"].append(player.dealers_hands[index][0].rank)
        output_obj["dealer_value"].append(player.dealers_value[index])
        output_obj["dealer_hand"].append(dealer_hand)

# Create a new dataframe that will be a pivot table for
# each player's starting hand and the dealer's first card
pivot_obj: dict[str, list[Union[str, int]]] = {
    "player": [],
    "starting_hand_value": [],
    "first_dealer_card": [],
    "win_count": [],
}
for player in tqdm(PLAYERS, disable=TQDM_DISABLED):
    # Create the object that will keep track for the
    # player where the key will be ranks for each pair
    player_obj: dict[frozenset[str], dict[str, int]] = {}
    for rank in constants.face_values:
        for second_rank in constants.face_values:
            # Create the frozenset pair as an entry
            player_obj[frozenset([rank, second_rank])] = {
                rank: 0 for rank in constants.face_values
            }

    # Iterate through the players winning games again
    # and collect the count of wins for the given hand
    for index in range(len(player.winning_value)):
        # Define the dealer's first card for the current winning hand
        dealers_first_card: str = player.dealers_hands[index][0].rank

        # Create a frozenset with the first two cards
        # in the player's winning hand
        first_two_frozenset: frozenset[str] = frozenset(
            [card.rank for card in player.winning_hands[index][0:2]]
        )

        # Increment the counter for the frozenset + dealer first
        # hand combinations
        player_obj[first_two_frozenset][dealers_first_card] += 1

    # Use the generated player object above to add to the dataframe object
    for first_two_frozenset, dealer_obj in player_obj.items():
        for dealers_first_card, win_count in dealer_obj.items():
            if win_count > 0:
                pivot_obj["player"].append(f"{player.name} (max={player.max_value})")
                pivot_obj["starting_hand_value"].append(",".join(first_two_frozenset))
                pivot_obj["first_dealer_card"].append(dealers_first_card)
                pivot_obj["win_count"].append(win_count)


# Write out to file with the dataframes
with pd.ExcelWriter("out/results.xlsx") as writer:
    """
    SUPPRESSING THIS OUTPUT BECAUSE IT WILL BE LARGE FOR
    LARGE VALUES OF GAMES

    pd.DataFrame(output_obj).to_excel(  # type: ignore
        writer,
        sheet_name="full_game",
        index=False,
    )
    """
    pivot_df = pd.DataFrame(pivot_obj)
    pivot_df.to_excel(  # type: ignore
        writer,
        sheet_name="pivot_obj",
        index=False,
    )

    # Pivot the dataframe
    pivoted_df = pd.pivot_table(  # type: ignore
        pivot_df,
        index=["player", "starting_hand_value"],
        columns="first_dealer_card",
        values="win_count",
        fill_value=0,
    )
    pivoted_df.to_excel(  # type: ignore
        writer,
        "final_pivot",
    )
