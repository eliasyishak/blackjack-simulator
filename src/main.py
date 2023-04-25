import random as r

from deck import Deck
from player import Player
from tqdm import tqdm

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
RUNS = 2
stats_obj: dict[Player, dict[str, int]] = {}

# Iterate through the number of runs specified
for _ in tqdm(range(RUNS)):
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
            player.won(dealers_hand=list(dealer.hand.cards_in_hand))
        # When the dealer has less than the player and the player has a
        # valid hand
        elif player.get_value() > dealer.get_value() and player.get_value() <= 21:
            player.won(dealers_hand=list(dealer.hand.cards_in_hand))
        else:
            dealer.won(dealers_hand=list(dealer.hand.cards_in_hand))

    # Reset the hand for each player after their game is over
    for game_player in current_players + [dealer]:
        game_player.reset_hand()
