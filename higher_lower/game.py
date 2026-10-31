from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from .cards import Card, Deck

HIGHER, LOWER = "h", "l"


@dataclass(frozen=True)
class Rules:
    starting_score: int = 50
    guesses_per_round: int = 8
    reward: int = 20
    penalty: int = 15


def is_correct(guess: str, current: Card, following: Card) -> bool:
    """A guess is right only if the next card is strictly higher/lower; ties lose."""
    if guess == HIGHER:
        return following.value > current.value
    if guess == LOWER:
        return following.value < current.value
    raise ValueError(f"invalid guess {guess!r}")


class Game:
    """Terminal game loop. Input/output are injectable so the game can be tested."""

    def __init__(
        self,
        rules: Rules = Rules(),
        rng: random.Random | None = None,
        ask: Callable[[str], str] = input,
        say: Callable[[str], None] = print,
    ) -> None:
        self.rules = rules
        self.rng = rng or random.Random()
        self.ask = ask
        self.say = say
        self.score = rules.starting_score

    def _ask_choice(self, prompt: str, choices: tuple[str, ...]) -> str:
        while True:
            answer = self.ask(prompt).strip().casefold()
            if answer in choices:
                return answer
            self.say(f"Please answer with {' or '.join(repr(c) for c in choices)}.")

    def play_round(self) -> None:
        deck = Deck(self.rng)
        deck.shuffle()
        current = deck.draw()
        self.say(f"\nThe first card is: {current}")

        for _ in range(self.rules.guesses_per_round):
            guess = self._ask_choice(f"Will the next card be higher or lower than {current}? (h/l): ", (HIGHER, LOWER))
            following = deck.draw()
            if following is None:  # cannot happen with the default rules, but keeps custom rules safe
                self.say("No more cards in the deck.")
                break

            self.say(f"The next card is: {following}")
            if is_correct(guess, current, following):
                self.score += self.rules.reward
                self.say(f"Correct! +{self.rules.reward}")
            else:
                self.score -= self.rules.penalty
                self.say(f"Wrong! -{self.rules.penalty}")
            self.say(f"Score: {self.score}")
            current = following

    def start(self) -> None:
        r = self.rules
        self.say("Welcome to Higher or Lower!")
        self.say("Guess whether the next card is higher or lower than the current one (Ace low, King high).")
        self.say(f"Right: +{r.reward} points. Wrong or tie: -{r.penalty} points. You start with {r.starting_score}.")

        while True:
            self.play_round()
            if self._ask_choice("\nPlay again? (y/n): ", ("y", "n")) == "n":
                self.say(f"Final score: {self.score}. Thanks for playing!")
                return
