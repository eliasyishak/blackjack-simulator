class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

        # Define the face value of the card as a list
        # since aces can be both 1 and 11
        self.value: list[int] = []
        if rank == "A":
            self.value.append(1)
            self.value.append(11)
        elif rank in ["J", "Q", "K"]:
            self.value.append(10)
        else:
            self.value.append(int(rank))

        print(self.value)

    def __repr__(self):
        value: str = ", ".join([str(v) for v in self.value])
        return f"{self.rank}-{self.suit} ({value})"
