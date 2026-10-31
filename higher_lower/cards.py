from __future__ import annotations

import random
from dataclasses import dataclass

SUITS = ("Spades", "Clubs", "Diamonds", "Hearts")
RANKS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def value(self) -> int:
        """Ace is low (1), King is high (13)."""
        return RANKS.index(self.rank) + 1

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    """A standard 52-card deck."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self) -> None:
        self._rng.shuffle(self.cards)

    def draw(self) -> Card | None:
        """Take the top card, or ``None`` if the deck is empty."""
        return self.cards.pop() if self.cards else None

    def __len__(self) -> int:
        return len(self.cards)
